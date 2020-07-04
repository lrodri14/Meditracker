from django.shortcuts import render
from .forms import *
from .models import *

# Create your views here.


def patients(request):
    patients_list = Patient
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
            patient_form.save(commit=False)

            allergies_form.save(commit=False)
            allergies_form.patient = patient_form
            allergies_form.save()

            antecedents_form.save(commit=False)
            antecedents_form.patient = patient_form
            antecedents_form.save()

            insurance_form.save(commit=False)
            insurance_form.patient = patient_form
            insurance_form.save()

            patient_form.save()
    else:
        patient_form = PatientForm
        allergies_form = AllergiesInformationForm
        antecedents_form = AntecedentForm
        insurance_form = InsuranceInformationForm
        template = 'patients/add_patient.html'
        context = {'patient_form': patient_form,
                   'allergies_form': allergies_form,
                   'insurance_form': insurance_form,
                   'antecedents_form': antecedents_form}
    return render(request, template, context=context)
