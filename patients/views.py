from django.http import JsonResponse
from django.shortcuts import render, redirect
from appointments.models import Consults
from django.template.loader import render_to_string
from .forms import *
from .models import *
from django.db.models import Q
from django.contrib.auth.models import Group
from django.core.paginator import Paginator
from appointments.forms import ConsultsDetailsFilterForm
from django.conf import settings

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
        template = 'patients/patients_partial_list.html'
        data = dict()
        if patient_filter.is_valid():
            if patient_filter.cleaned_data['patient'][0] in [str(x) for x in range(0, 9)]:
                context['patients'] = Patient.objects.filter(id_number__icontains=int(patient_filter.cleaned_data['patient']), created_by=request.user)
                data = {'html': render_to_string(template, context, request)}
            elif type(patient_filter.cleaned_data['patient']) == str:
                context['patients'] = Patient.objects.filter(Q(first_names__icontains=patient_filter.cleaned_data['patient']) | Q(last_names__icontains=patient_filter.cleaned_data['patient']), created_by=request.user)
                data = {'html': render_to_string(template, context, request)}
        return JsonResponse(data)
    return render(request, template, context=context)


def add_patient(request):
    if request.method == 'POST':
        patient_form = PatientForm(request.POST)
        allergies_form = AllergiesInformationFormset(request.POST)
        antecedents_form = AntecedentFormset(request.POST)
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
        allergies_form = AllergiesInformationFormset(queryset=Patient.objects.none())
        antecedents_form = AntecedentFormset(queryset=Patient.objects.none())
        insurance_form = InsuranceInformationForm
    return render(request, 'patients/add_patient.html', context={'patient_form': patient_form,
                                                                 'allergies_form': allergies_form,
                                                                 'insurance_form': insurance_form,
                                                                 'antecedents_form': antecedents_form})


def patient_details(request, pk):
    patient = Patient.objects.get(pk=pk)
    consults = Consults.objects.filter(patient=patient, created_by=request.user).order_by('-datetime')
    template = 'patients/patient_details.html'
    context = {'patient': patient, 'consults': consults, 'consults_form': ConsultsDetailsFilterForm}
    if request.method == 'POST':
        consults_form = ConsultsDetailsFilterForm(request.POST)
        if consults_form.is_valid():
            date_from = consults_form.cleaned_data['date_from']
            date_to = consults_form.cleaned_data['date_to']
            updated_consults = Consults.objects.filter(patient=patient, created_by=request.user, datetime__date__gte=date_from, datetime__date__lte=date_to)
            if len(updated_consults) > 0:
                context['consults'] = updated_consults
                for p in updated_consults:
                    print(p.datetime.date())
            else:
                context['error'] = 'No records found'
            data = dict()
            if request.headers['Filtertype'] == 'appointments':
                data = {'html': render_to_string('patients/patient_consults_partial_list.html', context, request)}
            elif request.headers['Filtertype'] == 'exams':
                data = {'html': render_to_string('patients/patient_exams_partial_list.html', context, request)}
            else:
                data = {'html': render_to_string('patients/patient_charges_partial_list.html', context, request)}
            return JsonResponse(data)
    return render(request, template, context)


def patient_delete(request, pk):
    patient = Patient.objects.get(pk=pk)
    doctor_group = Group.objects.get(name='Doctor')
    doctor = doctor_group in request.user.groups.all()
    consults = Consults.objects.filter(patient=patient, medical_status=True)
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
            patients = Patient.objects.filter(created_by=request.user)
            data = {'html': render_to_string(template, context, request=request),
                    'patients': render_to_string('patients/patients_partial_list.html', {'patients': patients, 'doctor': doctor}, request)}
    return JsonResponse(data)


def patient_update(request, pk):
    template = 'patients/patients_update.html'
    patient = Patient.objects.get(pk=pk)
    patient_allergies = AllergiesInformation.objects.get(patient=patient)
    patient_insurance = InsuranceInformation.objects.get(patient=patient)
    patient_antecedents = Antecedents.objects.get(patient=patient)
    patient_form = PatientForm(request.POST or None, instance=patient)
    allergies_form = AllergiesInformationForm(request.POST or None, instance=patient_allergies)
    insurance_form = InsuranceInformationForm(request.POST or None, instance=patient_insurance)
    antecedents_form = AntecedentForm(request.POST or None, instance=patient_antecedents)
    if request.method == 'POST':
        if patient_form.is_valid() and allergies_form.is_valid() and insurance_form.is_valid() and antecedents_form.is_valid():
            patient_form.save()
            allergies_form.save()
            insurance_form.save()
            antecedents_form.save()
            return redirect('patients:patients_details', pk=patient.pk)
    else:
        patient_form = PatientForm(instance=patient)
        allergies_form = AllergiesInformationFormset(queryset=Patient.objects.none())
        insurance_form = InsuranceInformationForm(instance=patient_insurance)
        antecedents_form = AntecedentFormset(queryset=Patient.objects.none())
    return render(request, template, context={'patient_form': patient_form, 'allergies_form': allergies_form,
                                                                            'insurance_form': insurance_form,
                                                                            'antecedents_form': antecedents_form})
