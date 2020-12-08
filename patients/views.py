"""
    This views.py file contains all the functions needed for the Patients app to perform. It contains 5 views,
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
from appointments.models import Consults, MedicalExams
from appointments.forms import ConsultsDetailsFilterForm


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
        The patients function is used to render all the patients related to this user, this function will first check
        if the user has the permissions to see this information, checking if it belongs to the Doctor group in the group
        class, afterwards it will retrieve all the patients related to this user and paginate them by 25 instances each
        page and also grab the filter form belonging to the Patients class, if the request.method attribute is a GET
        request, the function will render all this content and return the view if the request.method attribute is POST,
         it will populate the filter form with the content of the POST Request, if the form is valid, it will filter the
         patients with the given query and return all the instances found as a JsonResponse object, it receives a single
         parameter, 'request'.
    """
    doctor_group = Group.objects.get(name='Doctor')
    doctor = doctor_group in request.user.groups.all()
    today = timezone.localdate()
    template = 'patients/patients.html'
    patients_list = Patient.objects.filter(created_by=request.user).order_by('id_number')
    paginator = Paginator(patients_list, 17)
    page = request.GET.get('page')
    patients = paginator.get_page(page)
    patient_filter = PatientFilter
    context = {'patients': patients, 'doctor': doctor, 'form': patient_filter, 'today': today}
    if page:
        data = {'html': render_to_string('patients/patients_partial_list.html', context, request)}
        return JsonResponse(data)
    return render(request, template, context=context)


def filter_patients(request):
    query = request.META.get('HTTP_QUERY')
    doctor_group = Group.objects.get(name='Doctor')
    doctor = doctor_group in request.user.groups.all()
    today = timezone.localdate()
    template = 'patients/patients_filter_list.html'
    data = {}
    if query is not None:
        if len(query) > 0 and query[0] in [str(x) for x in range(0, 9)]:
            patients_list = Patient.objects.filter(id_number__icontains=int(query), created_by=request.user).order_by('id_number')
            paginator = Paginator(patients_list, 17)
            page = request.GET.get('page')
            updated_patients = paginator.get_page(page)
            context = {'patients': updated_patients, 'doctor': doctor, 'today': today, 'query':query}
            data = {'html': render_to_string(template, context, request)}
        elif type(query) == str:
            patients_list = Patient.objects.filter(Q(first_names__icontains=query) | Q(last_names__icontains=query), created_by=request.user).order_by('id_number')
            paginator = Paginator(patients_list, 17)
            page = request.GET.get('page')
            updated_patients = paginator.get_page(page)
            context = {'patients': updated_patients, 'doctor': doctor, 'today': today, 'query':query}
            data = {'html': render_to_string(template, context, request)}
    else:
        page = request.GET.get('page')
        query = request.GET.get('query')
        patients_list = Patient.objects.filter(Q(first_names__icontains=query) | Q(last_names__icontains=query), created_by=request.user).order_by('id_number')
        paginator = Paginator(patients_list, 17)
        updated_patients = paginator.get_page(page)
        context = {'patients': updated_patients, 'doctor': doctor, 'today': today, 'query': query}
        data = {'filtered_data': render_to_string(template, context, request)}
    return JsonResponse(data)


def add_patient(request):
    """
        DOCSTRING:
        The add_patients function is used to create Patient instances, this function will render four forms, the PatientForm
        used to render the personal information of the patient, the AllergiesFormset used to instance and relate as many
        allergies as needed to this particular patient, the AntecedentsFormset used to instance and relate as many
        antecedents as needed to this particular patient, and the InsuranceForm used to relate any insurance instance to
        this patient. It should be noted that the formsets are passed an empty queryset to the queryset paramater from the
        Formset class, this so the forms won't be pre-populated with any data. If the request.method is "GET" then the
        function will render the template with the before mentioned forms, if the request.method is "POST", then all the
        forms will be populated and checked if they are valid, if they are, they won't be commited yet, the function will
        check if there are any forms marked as deleted, if the form is not marked as deleted, then it's patient attribute
        is set to the current patient and saved, after all this process is completed, we will be redirected to the patients
        main page, it accepts one parameters, 'request'.
    """
    patient_form = PatientForm
    allergies_form = AllergiesInformationFormset(queryset=AllergiesInformation.objects.none())
    antecedents_form = AntecedentFormset(queryset=Antecedents.objects.none())
    insurance_form = InsuranceInformationForm()
    template = 'patients/add_patient.html'
    if request.method == 'POST':
        patient_form = PatientForm(request.POST)
        allergies_form = AllergiesInformationFormset(request.POST)
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
    allergies = AllergiesInformation.objects.filter(patient=patient)
    antecedents = Antecedents.objects.filter(patient=patient)
    insurance = InsuranceInformation.objects.get(patient=patient)
    consults = Consults.objects.filter(patient=patient, created_by=request.user).order_by('-datetime')
    charges = check_charges(consults)
    exams = MedicalExams.objects.filter(consult__patient=patient)
    template = 'patients/patient_details.html'
    context = {'patient': patient, 'consults': consults, 'allergies': allergies, 'antecedents': antecedents, 'insurance':insurance, 'exams': exams, 'charges': charges, 'consults_form': ConsultsDetailsFilterForm}
    if request.method == 'POST':
        consults_form = ConsultsDetailsFilterForm(request.POST)
        if consults_form.is_valid():
            date_from = consults_form.cleaned_data['date_from']
            date_to = consults_form.cleaned_data['date_to']
            updated_consults = Consults.objects.filter(patient=patient, created_by=request.user, datetime__date__gte=date_from, datetime__date__lte=date_to)
            updated_exams = MedicalExams.objects.filter(consult__patient=patient, consult__datetime__date__gte=date_from, consult__datetime__date__lte=date_to)
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


def patient_delete(request, pk):
    """
        DOCSTRING:
        The patient_delete function is used to delete Patient instances, a particular functionality of this function
        is that it will lookup if there is any data related to this patient, if there is not, the patient will be de-
        leted successfully, else, an error will be raised, this to protect the data integrity, it will retrieve the
        updated list of patients and render a new template with this content, this data will be returned as a
        JsonResponse, it accepts two parameters, 'request' and 'pk' which expects an patients instance pk.

    """
    today = timezone.localdate()
    patient = Patient.objects.get(pk=pk)
    doctor_group = Group.objects.get(name='Doctor')
    doctor = doctor_group in request.user.groups.all()
    consults = Consults.objects.filter(created_by=request.user, patient=patient, medical_status=True)
    template = 'patients/patients_delete.html'
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
            page = request.GET.get('page')
            patients = paginator.get_page(page)
            data = {'html': render_to_string(template, context, request=request),
                    'patients': render_to_string('patients/patients_partial_list.html', {'patients': patients, 'doctor': doctor, 'today': today}, request)}
    return JsonResponse(data)


def patient_update(request, pk):
    """
        DOCSTRING:
        The update_patients function is used to update Patient instances, this function will render four forms, the PatientForm
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

    template = 'patients/patients_update.html'
    patient = Patient.objects.get(pk=pk)
    patient_insurance = InsuranceInformation.objects.get(patient=patient)
    patient_form = PatientForm(request.POST or None, instance=patient)
    allergies_form = AllergiesInformationUpdateFormset(instance=patient)
    insurance_form = InsuranceInformationForm(request.POST or None, instance=patient_insurance)
    antecedents_form = AntecedentUpdateFormset(instance=patient)
    if request.method == 'POST':
        patient_form = PatientForm(request.POST or None, instance=patient)
        allergies_form = AllergiesInformationUpdateFormset(request.POST, instance=patient)
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
