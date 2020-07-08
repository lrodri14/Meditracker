from django.shortcuts import render, redirect, reverse
from .forms import *
from .models import *
from django.db import IntegrityError

# Create your views here.


def patients(request):
    patients_list = Patient.objects.all()
    template = 'patients/patients.html'
    context = {'patients': patients_list}
    return render(request, template, context=context)


def add_patient(request):
    if request.method == 'POST':
        patient_form = PatientForm(request.POST)
        allergies_form = AllergiesInformationForm(request.POST)
        antecedents_form = AntecedentForm(request.POST)
        insurance_form = InsuranceInformationForm(request.POST)
        if patient_form.is_valid() and allergies_form.is_valid() and antecedents_form.is_valid() and insurance_form.is_valid():
            patient = patient_form.save()
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
    template = 'patients/patients_delete.html'
    if request.method == 'POST':
        if request.POST['choice'] == 'yes':
            patient.delete()
            return redirect('patients:patients')
        else:
            return redirect('patients:patients_details', pk=patient.pk)
    return render(request, template, context={'patient': patient})


def patient_update(request, pk):
    template = 'patients/patients_update.html'
    patient = Patient.objects.get(pk=pk)
    patient_allergies = AllergiesInformation.objects.get(patient=patient)
    patient_insurance = InsuranceInformation.objects.get(patient=patient)
    patient_antecedents = Antecedents.objects.get(patient=patient)
    patient_form = PatientForm(request.POST, instance=patient)
    allergies_form = AllergiesInformationForm(request.POST, instance=patient_allergies)
    insurance_form = InsuranceInformationForm(request.POST, instance=patient_insurance)
    antecedents_form = AntecedentForm(request.POST, instance=patient_antecedents)
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


def insurance_list(request):
    insurances_list = InsuranceCarrier.objects.filter(country=request.user.profile.origin)
    context = {'insurance_list': insurances_list, 'origin': request.user.profile.origin}
    template = 'patients/insurance_list.html'
    return render(request, template, context=context)


def add_insurance_carrier(request):
    insurance_carrier_form = InsuranceCarrierForm
    context = {'insurance_carrier_form': insurance_carrier_form}
    template = 'patients/insurance_add.html'
    if request.method == 'POST':
        insurance_form = InsuranceCarrierForm(request.POST)
        if insurance_form.is_valid():
            try:
                insurance_form.save()
            except IntegrityError:
                context['unique_error'] = '*This company is already registered for this region.'
                return render(request, template, context)
    return render(request, template, context)


def insurance_delete(request, pk):
    carrier = InsuranceCarrier.objects.get(pk=pk)
    context = {'insurance': carrier}
    template = 'patients/insurance_delete.html'
    if request.POST:
        pass
    else:
        return redirect(reverse('patients:insurance_list'))
    return render(request, template, context)


def insurance_update(request):
    pass


def allergies_list(request):
    pass


def allergies_create(request):
    pass


def allergies_delete(request):
    pass


def allergies_update(request):
    pass




