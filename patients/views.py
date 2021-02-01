"""
    This views.py file contains all the functions needed for the Patients app to perform. It contains 6 views,
    which perform the CRUD Operations for our Patients Class, and a function used to check if there are charges or not.
"""

# Imports

import datetime
from .forms import *
from .models import *
from django.db.models import Q
from django.http import JsonResponse
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from accounts.models import MailingCredential
from django.template.loader import render_to_string
from appointments.models import Consult, MedicalTestResult
from appointments.forms import ConsultDetailsFilterForm
from utilities.accounts_utilities import open_connection
from utilities.global_utilities import country_number_codes, collect_country_code
from smtplib import SMTPSenderRefused, SMTPAuthenticationError, SMTPNotSupportedError

# Create your views here.


def patients(request):
    """
        DOCSTRING:
        The patients function is used to display all the patients belonging to this user, first the view will check if the
        user belongs to the doctor group searching in the users groups, afterwards it will collect all the patients that are
        related to him and paginate them in groups of 17 instances, the patient filtering form will also be sent for rendering,
        this function only accepts 'GET' requests, the 'page' query parameter will be evaluated every time, so the function knows
        which page should it send, if the 'page' parameter exists, then the content will be returned in JSON Format. It accepts only
        one parameter, 'request' which expects a request object.
    """
    doctor_group = Group.objects.get(name='Doctor')
    doctor = doctor_group in request.user.groups.all()
    template = 'patients/patients.html'
    patients_list = Patient.objects.filter(created_by=request.user).order_by('id_number')
    patient_filter = PatientFilterForm
    context = {'patients': patients_list, 'form': patient_filter, 'doctor': doctor}
    return render(request, template, context)


def filter_patients(request):
    """
        DOCSTRING:
        The filter_patients function is used to filter the patients belonging to the user based on a query sent through
        'GET' request in the 'query' parameter, once this data is collected, it is paginated by 17 instances each page, we also need
        to evaluate the 'page' parameter, so the function knows which page must be sent to the front-end, the data collected
        is sent in JSON Format.
    """
    doctor_group = Group.objects.get(name='Doctor')
    doctor = doctor_group in request.user.groups.all()
    template = 'patients/patients_partial_list.html'
    query = request.GET.get('query')
    patients_list = Patient.objects.filter(Q(first_names__icontains=query) | Q(last_names__icontains=query), created_by=request.user).order_by('id_number')
    context = {'patients': patients_list, 'doctor': doctor, 'filtered': True}
    data = {'html': render_to_string(template, context, request)}
    return JsonResponse(data)


def add_patient(request):
    """
        DOCSTRING:
        The add_patients function is used to create Patient instances, this function will render four forms, the PatientForm
        used to render the personal information of the patient, the AllergiesFormset used to instance and relate as many
        allergies as needed to this particular patient, the AntecedentsFormset used to instance and relate as many
        antecedents as needed to this particular patient, and the InsuranceForm used to relate any insurance instance to
        this patient. It should be noted that the formsets are passed an empty queryset to the queryset parameter from the
        Formset class, this so the forms won't be pre-populated with any data. If the request.method is "GET" then the
        function will render the template with the before mentioned forms, if the request.method is "POST", then all the
        forms will be populated and checked if they are valid, if they are, they won't be commited yet, the function will
        check if there are any forms marked as deleted, if the form is not marked as deleted, then it's patient attribute
        is set to the current patient and saved, after all this process is completed, we will be redirected to the patients
        main page, it accepts one parameters, 'request'.
    """
    patient_form = PatientForm(initial={'phone_number': country_number_codes[request.user.profile.location]})
    allergies_form = AllergyInformationFormset(queryset=AllergyInformation.objects.none())
    antecedents_form = AntecedentFormset(queryset=Antecedent.objects.none())
    insurance_form = InsuranceInformationForm()
    template = 'patients/add_patient.html'
    if request.method == 'POST':
        patient_form = PatientForm(request.POST)
        allergies_form = AllergyInformationFormset(request.POST)
        antecedents_form = AntecedentFormset(request.POST)
        insurance_form = InsuranceInformationForm(request.POST)
        if patient_form.is_valid() and allergies_form.is_valid() and antecedents_form.is_valid() and insurance_form.is_valid():
            patient = patient_form.save(commit=False)
            allergies_instances = allergies_form.save(commit=False)
            antecedents_instances = antecedents_form.save(commit=False)
            insurance = insurance_form.save(commit=False)

            if patient.phone_number is None:
                patient.phone_number = country_number_codes[request.user.profile.location]
            patient.save()
            patient.created_by = request.user
            patient.save()

            for allergy_form in allergies_instances:
                if allergy_form in allergies_form.deleted_objects:
                    allergy_form.delete()
                else:
                    allergy_form.patient = patient
                    allergy_form.save()

            for antecedent_form in antecedents_instances:
                if antecedent_form in antecedents_form.deleted_objects:
                    antecedent_form.delete()
                else:
                    antecedent_form.patient = patient
                    antecedent_form.save()

            insurance.patient = patient
            insurance.save()

            return redirect('patients:patients')

    context_data = {'patient_form': patient_form, 'allergies_form': allergies_form, 'insurance_form': insurance_form, 'antecedents_form': antecedents_form, 'country_code': 'flag-icon-' + request.user.profile.location.lower()}
    return render(request, template, context=context_data)


def patient_details(request, pk):
    """
        DOCSTRING:
        The patient_details function is used to render the patient details and all the data related to this patient, as the
        consults, exams, and charges, and the personal information as well as antecedents and insurance information,
        this function will also render a filtering form for this content, if the request.method attribute is "GET" then
        this information as well as the filter forms will be rendered in the template, if the request.method is a POST,
        it will populate this form with the POST data, and extract the information through the cleaned_data dictionary
        attribute from forms, if there were results found, it will return the data, but if not, a custom error will be
        raised. All this data is return as a JsonResponse object. This function accepts two parameters, 'request' and
        a 'pk' which expects a patient instance pk.
    """
    patient = Patient.objects.get(pk=pk)
    allergies = AllergyInformation.objects.filter(patient=patient)
    antecedents = Antecedent.objects.filter(patient=patient)
    insurance = InsuranceInformation.objects.get(patient=patient)
    consults_list = Consult.objects.filter(patient=patient, created_by=request.user).order_by('-datetime')
    charges_list = Consult.objects.filter(patient=patient, created_by=request.user, charge__gte=0).order_by('-datetime')
    exams_list = MedicalTestResult.objects.filter(consult__patient=patient).order_by('-date')
    template = 'patients/patient_details.html'
    context = {'patient': patient, 'consults': consults_list, 'allergies': allergies, 'antecedents': antecedents, 'insurance':insurance, 'exams': exams_list, 'charges': charges_list, 'consults_form': ConsultDetailsFilterForm}
    return render(request, template, context)


def filter_patient_details(request):
    """
        DOCSTRING:
        The filter_patient_details view is used to filter the details either of appoinments, exams or charges of a speci-
        fic patient, the request url contains some parameters we must extract, these are the request_details, the
        date_from and the date_to key values, they are used to filter the results between those dates, the results of that
        filtering will be paginated in groups of 16 items, the response will be sent in JSON Format, using the JsonRes-
        ponse class.
    """
    date_from = datetime.datetime.strptime(request.GET.get('date_from'), '%Y-%m-%d')
    date_to = datetime.datetime.strptime(request.GET.get('date_to'), '%Y-%m-%d')
    requested_details = request.GET.get('filter_request_type')
    if requested_details == 'appointments':
        filtered_results = Consult.objects.filter(datetime__date__gte=date_from, datetime__date__lte=date_to, created_by=request.user).order_by('-datetime')
        template = 'patients/patient_consults_partial_list.html'
        context = {'consults': filtered_results, 'filtered': True}
        data = {'html': render_to_string(template, context, request)}
    elif requested_details == 'charges':
        filtered_results = Consult.objects.filter(datetime__date__gte=date_from, datetime__date__lte=date_to, created_by=request.user, charge__gte=0).order_by('-datetime')
        template = 'patients/patient_charges_partial_list.html'
        context = {'charges': filtered_results, 'filtered': True}
        data = {'html': render_to_string(template, context, request)}
    else:
        filtered_results = MedicalTestResult.objects.filter(date__gte=date_from, date__lte=date_to, consult__created_by=request.user).order_by('-date')
        template = 'patients/patient_exams_partial_list.html'
        context = {'exams': filtered_results, 'filtered': True}
        data = {'html': render_to_string(template, context, request)}
    return JsonResponse(data)


def delete_patient(request, pk):
    """
        DOCSTRING:
        The delete_patient function is used to delete Patient instances, a particular functionality of this function
        is that it will lookup if there is any data related to this patient, if there is not, the patient will be de-
        leted successfully, else, an error will be raised, this to protect the data integrity, it will retrieve the
        updated list of patients and render a new template with this content, this data will be returned as a
        JsonResponse, it accepts two parameters, 'request' and 'pk' which expects an patients instance pk.

    """
    patient = Patient.objects.get(pk=pk)
    doctor_group = Group.objects.get(name='Doctor')
    doctor = doctor_group in request.user.groups.all()
    consults = Consult.objects.filter(created_by=request.user, patient=patient, medical_status=True)
    template = 'patients/delete_patient.html'
    context = {'patient': patient}
    data = {'html': render_to_string(template, context, request=request)}
    if request.method == 'POST':
        if len(consults) > 0:
            context = {'error': 'Patient linked to {} records, deletion prohibited'.format(len(consults))}
            data = {'html': render_to_string(template, context, request)}
        else:
            patient.delete()
            context = {'patient_deleted': ' Patient has been deleted successfully'}
            patients_list = Patient.objects.filter(created_by=request.user).order_by('id_number')
            paginator = Paginator(patients_list, 17)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            data = {'html': render_to_string(template, context, request),
                    'patients': render_to_string('patients/patients_list.html', {'patients': page_obj, 'doctor': doctor}, request)}
    return JsonResponse(data)


def update_patient(request, pk):
    """
        DOCSTRING:
        The update_patient function is used to update Patient instances, this function will render four forms, the PatientForm
        used to update the personal information of the patient, the AllergiesFormset used to instance and relate as many
        allergies as needed to this particular patient, the AntecedentsFormset used to instance and relate as many
        antecedents as needed to this particular patient, and the InsuranceForm used to relate any insurance instance to
        this patient. It should be noted that the formsets are passed an instance attribute set to the user this so the
        forms will be pre-populated with user related data. If the request.method is "GET" then the function will render
        the template with the before mentioned forms, if the request.method is "POST", then all the forms will be populated
        and checked if they are valid, if they are, they won't be commited yet, the function will check if there are any
        forms marked as deleted, if the form is not marked as deleted, then it's patient attribute is set to the current
        patient and saved, after all this process is completed, we will be redirected to the patients main page,
        it accepts one parameters, 'request'.
    """

    template = 'patients/update_patient.html'
    patient = Patient.objects.get(pk=pk)
    patient_insurance = InsuranceInformation.objects.get(patient=patient)
    patient_form = PatientForm(request.POST or None, instance=patient)
    allergies_form = AllergyInformationUpdateFormset(instance=patient)
    insurance_form = InsuranceInformationForm(request.POST or None, instance=patient_insurance)
    antecedents_form = AntecedentUpdateFormset(instance=patient)
    if request.method == 'POST':
        patient_form = PatientForm(request.POST or None, instance=patient)
        allergies_form = AllergyInformationUpdateFormset(request.POST, instance=patient)
        insurance_form = InsuranceInformationForm(request.POST, instance=patient_insurance)
        antecedents_form = AntecedentUpdateFormset(request.POST, instance=patient)
        if patient_form.is_valid() and allergies_form.is_valid() and insurance_form.is_valid() and antecedents_form.is_valid():
            patient = patient_form.save(commit=False)
            if patient.phone_number is None:
                patient.phone_number = country_number_codes[request.user.profile.location]
            patient.save()
            allergies_form.save()
            insurance_form.save()
            antecedents_form.save()
            return redirect('patients:patients_details', pk=patient.pk)
    return render(request, template, context={'patient_form': patient_form, 'allergies_form': allergies_form,
                                                                            'insurance_form': insurance_form,
                                                                            'antecedents_form': antecedents_form,
                                                                            'country_code': 'flag-icon-' + collect_country_code(patient.phone_number, request.user)})


def send_email(request, pk):
    """
        DOCSTRING:
        The send_email function is used to send emails to the patient whenever is needed, this function takes two args
        the request itself and the pk of a specific patient, used to grab it's email, if the request.method is the same
        as 'GET' then the form will be displayed, the content will return in JSON Format using the JsonResponse class,
        if the request.method attribute is the same as 'POST', then the following will happen:
        - Grab the user Mailing Credentials
        - We will open a connection using the open_connection function and we will pass the credential as its params
        - We will collect the email subject and body
        - Finally if no errors occur, our message will be sent using the send_mail function
        - If errors occur, a proper error will be displayed to the user.
    """
    template = 'patients/email_form.html'
    patient = Patient.objects.get(pk=pk)
    context = {'form': EmailForm, 'receiver': patient, 'today': timezone.localdate()}
    data = {'html': render_to_string(template, context, request)}
    if request.POST:
        mailing_credentials = MailingCredential.objects.get(user=request.user)
        connection = open_connection(mailing_credentials)
        sender = mailing_credentials.email
        receiver = patient.email
        subject = request.POST.get('subject')
        message = request.POST.get('body')
        try:
            send_mail(subject, message, sender, (receiver,), connection=connection, fail_silently=False)
            context = {'success': 'Email has been sent successfully'}
        except ConnectionRefusedError:
            context = {'error': 'SMTP Server not configured, set up your credentials in settings'}
        except SMTPSenderRefused:
            context = {'error': 'Incomplete credentials in SMTP Server settings'}
        except SMTPAuthenticationError:
            context = {'error': 'Incorrect credentials in SMTP Server Settings'}
        except SMTPNotSupportedError:
            context = {'error': 'TLS Protocol must be active to open connection'}
        data = {'html': render_to_string(template, context, request)}
        return JsonResponse(data)
    return JsonResponse(data)
