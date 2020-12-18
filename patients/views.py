"""
    This views.py file contains all the functions needed for the Patients app to perform. It contains 6 views,
    which perform the CRUD Operations for our Patients Class, and a function used to check if there are charges or not.
"""

# Imports
from .forms import *
from .models import *
from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from appointments.models import Consult, MedicalExam
from appointments.forms import ConsultDetailsFilterForm


# Functions

def check_charges(consults):
    """
        DOCSTRING:
        This function is used to check if there are any charges inside the consults, if there are not then the
        charges section of the patient details would not be rendered. It takes a single argument: 'consults' and
        it expects a querySet.
    """
    charges = None
    for c in consults:
        if c.charge:
            charges = True
            break
    return charges


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
    paginator = Paginator(patients_list, 17)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    patient_filter = PatientFilterForm
    context = {'patients': page_obj, 'form': patient_filter, 'doctor': doctor}
    if page_number:
        data = {'html': render_to_string('patients/patients_partial_list.html', context, request)}
        return JsonResponse(data)
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
    page_number = request.GET.get('page')
    patients_list = Patient.objects.filter(Q(first_names__icontains=query) | Q(last_names__icontains=query), created_by=request.user).order_by('id_number')
    paginator = Paginator(patients_list, 17)
    page_obj = paginator.get_page(page_number)
    context = {'patients': page_obj, 'doctor': doctor, 'filtered': True}
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
    patient_form = PatientForm
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

    context_data = {'patient_form': patient_form, 'allergies_form': allergies_form, 'insurance_form': insurance_form, 'antecedents_form': antecedents_form}
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
    consults = Consult.objects.filter(patient=patient, created_by=request.user).order_by('-datetime')
    charges = check_charges(consults)
    exams = MedicalExam.objects.filter(consult__patient=patient)
    template = 'patients/patient_details.html'
    context = {'patient': patient, 'consults': consults, 'allergies': allergies, 'antecedents': antecedents, 'insurance':insurance, 'exams': exams, 'charges': charges, 'consults_form': ConsultDetailsFilterForm}
    if request.method == 'POST':
        consults_form = ConsultDetailsFilterForm(request.POST)
        if consults_form.is_valid():
            date_from = consults_form.cleaned_data['date_from']
            date_to = consults_form.cleaned_data['date_to']
            updated_consults = Consult.objects.filter(patient=patient, created_by=request.user, datetime__date__gte=date_from, datetime__date__lte=date_to)
            updated_exams = MedicalExam.objects.filter(consult__patient=patient, consult__datetime__date__gte=date_from, consult__datetime__date__lte=date_to)
            if len(updated_consults) > 0:
                context['consults'] = updated_consults
                context['exams'] = updated_exams
                for p in updated_consults:
                    print(p.datetime.date())
            else:
                context['error'] = 'No records found'
            if request.headers['Filtertype'] == 'appointments':
                data = {'html': render_to_string('patients/patient_consults_partial_list.html', context, request)}
            elif request.headers['Filtertype'] == 'exams':
                data = {'html': render_to_string('patients/patient_exams_partial_list.html', context, request)}
            else:
                data = {'html': render_to_string('patients/patient_charges_partial_list.html', context, request)}
            return JsonResponse(data)
    return render(request, template, context)


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
            context = {'error': 'Sorry this patient can not be deleted, it is linked to {} records'.format(len(consults))}
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
            patient_form.save()
            allergies_form.save()
            insurance_form.save()
            antecedents_form.save()
            return redirect('patients:patients_details', pk=patient.pk)
    return render(request, template, context={'patient_form': patient_form, 'allergies_form': allergies_form,
                                                                            'insurance_form': insurance_form,
                                                                            'antecedents_form': antecedents_form})
