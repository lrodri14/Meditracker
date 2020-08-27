from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse
from appointments.models import Consults
from django.template.loader import render_to_string
from .forms import *
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group
from django.core.paginator import Paginator

# Create your views here.


def patients(request):
    doctor_group = Group.objects.get(name='Doctor')
    doctor = doctor_group in request.user.groups.all()
    patients_list = Patient.objects.filter(created_by=request.user).order_by('id_number')
    paginator = Paginator(patients_list, 25)
    page = request.GET.get('page')
    patients = paginator.get_page(page)
    patient_filter = PatientFilter
    template = 'patients/patients.html'
    context = {'patients': patients, 'doctor': doctor, 'form': patient_filter}
    if request.method == 'POST':
        patient_filter = PatientFilter(request.POST)
        if patient_filter.is_valid():
            if patient_filter.cleaned_data['patient'][0] in [str(x) for x in range(0, 11)]:
                context['patients'] = Patient.objects.filter(id_number__icontains=int(patient_filter.cleaned_data['patient']), created_by=request.user)
                return render(request, template, context)
            elif type(patient_filter.cleaned_data['patient']) == str:
                context['patients'] = Patient.objects.filter(first_names__icontains=patient_filter.cleaned_data['patient'], created_by=request.user)
                return render(request, template, context)
    return render(request, template, context=context)


def add_patient(request):
    if request.method == 'POST':
        patient_form = PatientForm(request.POST)
        allergies_form = AllergiesInformationForm(request.POST)
        antecedents_form = AntecedentForm(request.POST)
        insurance_form = InsuranceInformationForm(request.POST)
        if patient_form.is_valid() and allergies_form.is_valid() and antecedents_form.is_valid() and insurance_form.is_valid():
            patient = patient_form.save(commit=False)
            patient.created_by = request.user
            patient.save()

            allergies = allergies_form.save(commit=False)
            allergies.patient = patient
            allergies.save()

            antecedents = antecedents_form.save(commit=False)
            antecedents.patient = patient
            antecedents.save()

            insurance = insurance_form.save(commit=False)
            insurance.patient = patient
            insurance.save()
            return redirect('patients:patients')
    else:
        patient_form = PatientForm
        allergies_form = AllergiesInformationForm
        antecedents_form = AntecedentForm
        insurance_form = InsuranceInformationForm
    return render(request, 'patients/add_patient.html', context={'patient_form': patient_form,
                                                                 'allergies_form': allergies_form,
                                                                 'insurance_form': insurance_form,
                                                                 'antecedents_form': antecedents_form})


def patient_details(request, pk):
    patient = Patient.objects.get(pk=pk)
    template = 'patients/patient_details.html'
    return render(request, template, context={'patient': patient})


def patient_delete(request, pk):
    patient = Patient.objects.get(pk=pk)
    patients = Patient.objects.filter(created_by=request.user)
    doctor_group = Group.objects.get(name='Doctor')
    doctor = doctor_group in request.user.groups.all()
    consults = Consults.objects.filter(patient=patient)
    template = 'patients/patients_delete.html'
    context = {'patient': patient}
    data = {'html': render_to_string(template, context, request=request)}
    if request.method == 'POST':
        if len(consults) > 0:
            context = {'error': 'Sorry this patient can not be deleted, it is linked to {} records'.format(len(consults))}
        else:
            patient.delete()
            context = {'patient_deleted': ' Patient has been deleted successfully'}
            data = {'html': render_to_string(template, context, request=request),
                    'patients': render_to_string('patients/patients_partial_list.html', {'patients':patients, 'doctor': doctor}, request)}
    return JsonResponse(data)


def patient_update(request, pk):
    template = 'patients/patients_update.html'
    patient = Patient.objects.get(pk=pk)
    patient_allergies = AllergiesInformation.objects.get(patient=patient)
    patient_insurance = InsuranceInformation.objects.get(patient=patient)
    patient_antecedents = Antecedents.objects.get(patient=patient)
    patient_form = PatientForm(instance=patient)
    allergies_form = AllergiesInformationForm(instance=patient_allergies)
    insurance_form = InsuranceInformationForm(instance=patient_insurance)
    antecedents_form = AntecedentForm(instance=patient_antecedents)
    if request.method == 'POST':
        if patient_form.is_valid() and allergies_form.is_valid() and insurance_form.is_valid() and antecedents_form.is_valid():
            patient_form.save()
            allergies_form.save()
            insurance_form.save()
            antecedents_form.save()
            return redirect('patients:patients_details', pk=patient.pk)
    else:
        patient_form = PatientForm(instance=patient)
        allergies_form = AllergiesInformationForm(instance=patient_allergies)
        insurance_form = InsuranceInformationForm(instance=patient_insurance)
        antecedents_form = AntecedentForm(instance=patient_antecedents)
    return render(request, template, context={'patient_form': patient_form, 'allergies_form': allergies_form,
                                                                            'insurance_form': insurance_form,
                                                                            'antecedents_form': antecedents_form})
