from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.apps import apps
from django.template.loader import render_to_string
from patients import forms
from appointments.forms import DrugsForm, DrugsFilterForm
InsuranceCarrier = apps.get_model('patients', 'InsuranceCarrier')
Drugs = apps.get_model('appointments', 'Drugs')
Allergies = apps.get_model('patients', 'Allergies')


# Create your views here.

# Settings

def settings(request):
    template = 'settings/settings.html'
    insurances_list = InsuranceCarrier.objects.filter(country=request.user.profile.origin)[:5]
    allergies_created_list = Allergies.objects.all()[:5]
    drugs_list = Drugs.objects.filter(created_by=request.user)[:5]
    context = {'insurance_list': insurances_list, 'allergies_list': allergies_created_list, 'drugs_list': drugs_list}
    return render(request, template, context)

# Insurances


def insurance_list(request):
    insurances_list = InsuranceCarrier.objects.filter(created_by=request.user)
    template = 'settings/insurance_list.html'
    context = {'insurances': insurances_list, 'form': forms.InsuranceCarrierFilterForm}
    data = {'html': render_to_string(template, context, request)}
    if request.method == 'POST':
        filter_form = forms.InsuranceCarrierFilterForm(request.POST)
        if filter_form.is_valid():
            updated_insurances = InsuranceCarrier.objects.filter(created_by=request.user, company__icontains=filter_form.cleaned_data['company'])
            if len(updated_insurances) > 0:
                context['insurances'] = updated_insurances
                data = {'updated_html': render_to_string(template, context, request)}
    return JsonResponse(data)


def add_insurance_carrier(request):
    insurance_carrier_form = forms.InsuranceCarrierForm
    context = {'insurance_carrier_form': insurance_carrier_form}
    template = 'settings/insurance_add.html'
    data = {'html': render_to_string(template, context, request)}
    if request.method == 'POST':
        insurance_form = forms.InsuranceCarrierForm(request.POST)
        if insurance_form.is_valid():
            try:
                insurance = insurance_form.save(commit=False)
                insurance.created_by = request.user
                insurance.save()
                updated_insurances = InsuranceCarrier.objects.filter(created_by=request.user)
                context = {'insurances': updated_insurances, 'form': forms.InsuranceCarrierFilterForm}
                # How to return an error from the backend to the frontend?
                data = {'updated_html': render_to_string('settings/insurance_list.html', context, request)}
            except IntegrityError:
                context['error'] = 'This insurance is already listed'
                data = {'html': render_to_string(template, context, request)}
    return JsonResponse(data)


def insurance_details(request, pk):
    carrier = InsuranceCarrier.objects.get(pk=pk)
    template = 'settings/insurance_details.html'
    context = {'insurance': carrier}
    data = {'html': render_to_string(template, context, request)}
    return JsonResponse(data)


def insurance_update(request, pk):
    carrier = InsuranceCarrier.objects.get(pk=pk)
    insurance_form = forms.InsuranceCarrierForm(request.POST or None, instance=carrier)
    template = 'settings/insurance_update.html'
    context = {'insurance': insurance_form, 'carrier':carrier}
    data = {'html': render_to_string(template, context, request)}
    if request.method == 'POST':
        insurance_form = forms.InsuranceCarrierForm(request.POST or None, instance=carrier)
        if insurance_form.is_valid():
            try:
                # Why do i need to provide again the user?
                insurance_form.save()
                updated_insurances = InsuranceCarrier.objects.filter(created_by=request.user)
                context = {'insurances': updated_insurances, 'form': forms.InsuranceCarrierFilterForm}
                # How to return an error from the backend to the frontend?
                data = {'updated_html': render_to_string('settings/insurance_list.html', context, request)}
            except IntegrityError:
                context['error'] = 'This insurance is already listed'
                data = {'html': render_to_string(template, context, request)}
    return JsonResponse(data)


def insurance_delete(request, pk):
    carrier = InsuranceCarrier.objects.get(pk=pk)
    context = {'insurance': carrier}
    template = 'settings/insurance_delete.html'
    data = {'html': render_to_string(template, context, request)}
    if request.method == 'POST':
            carrier.delete()
            updated_insurances = InsuranceCarrier.objects.filter(created_by=request.user)
            context = {'insurances': updated_insurances, 'form': forms.InsuranceCarrierFilterForm}
            # How to return an error from the backend to the frontend?
            data = {'updated_html': render_to_string('settings/insurance_list.html', context, request)}
    return JsonResponse(data)


# Allergies

def allergies_list(request):
    allergies_created = Allergies.objects.filter(created_by=request.user)
    template = 'settings/allergies_list.html'
    context = {'allergies': allergies_created, 'form': forms.AllergiesFilterForm}
    data = {'html': render_to_string(template, context, request)}
    if request.method == 'POST':
        filter_form = forms.AllergiesFilterForm(request.POST)
        if filter_form.is_valid():
            updated_allergies = Allergies.objects.filter(created_by=request.user, allergy_type__icontains=filter_form.cleaned_data['allergy_type'])
            if len(updated_allergies) > 0:
                context['allergies'] = updated_allergies
                data = {'updated_html': render_to_string(template, context, request)}
    return JsonResponse(data)


def allergies_create(request):
    allergies_form = forms.AllergiesForm
    template = 'settings/add_allergies.html'
    context = {'allergies_form': allergies_form}
    data = {'html': render_to_string(template, context, request)}
    if request.method == 'POST':
        allergies_form = forms.AllergiesForm(request.POST)
        if allergies_form.is_valid():
            try:
                allergy = allergies_form.save(commit=False)
                allergy.created_by = request.user
                allergy.save()
                allergies = Allergies.objects.filter(created_by=request.user)
                context = {'allergies': allergies,'form': forms.AllergiesFilterForm}
                data = {'updated_html': render_to_string('settings/allergies_list.html', context, request)}
            except IntegrityError:
                context['error'] = 'This allergy is already in your options'
                data = {'html': render_to_string('settings/allergies_list.html', context, request)}
    return JsonResponse(data)


def allergies_details(request, pk):
    allergy = Allergies.objects.get(pk=pk)
    template = 'settings/allergy_details.html'
    context = {'allergy': allergy}
    data = {'html': render_to_string(template, context, request)}
    return JsonResponse(data)


def allergies_update(request, pk):
    allergy = Allergies.objects.get(pk=pk)
    template = 'settings/update_allergy.html'
    allergy_form = forms.AllergiesForm(request.POST or None, instance=allergy)
    context = {'allergy': allergy, 'allergy_form': allergy_form}
    data = {'html': render_to_string(template, context, request)}
    if request.method == 'POST':
        allergy_form = forms.AllergiesForm(request.POST or None, instance=allergy)
        if allergy_form.is_valid():
            try:
                allergy = allergy_form.save(commit=False)
                allergy.created_by = request.user
                allergy.save()
                allergies = Allergies.objects.filter(created_by=request.user)
                context = {'allergies': allergies, 'form': forms.AllergiesFilterForm}
                data = {'updated_html': render_to_string('settings/allergies_list.html', context, request)}
            except IntegrityError:
                context['error'] = 'This allergy is already in your options'
                data = {'html': render_to_string(template, context, request)}
    return JsonResponse(data)


def allergies_delete(request, pk):
    allergy = Allergies.objects.get(pk=pk)
    template = 'settings/allergy_delete.html'
    context = {'allergy': allergy}
    data = {'html': render_to_string(template, context, request)}
    if request.method == 'POST':
            allergy.delete()
            allergies = Allergies.objects.filter(created_by=request.user)
            context = {'allergies': allergies, 'form': forms.AllergiesFilterForm}
            data = {'updated_html': render_to_string('settings/allergies_list.html', context, request)}
    return JsonResponse(data)


# Drugs


def drugs_list(request):
    drugs_list = Drugs.objects.filter(created_by=request.user)
    template = 'settings/drugs_list.html'
    context = {'drugs': drugs_list, 'form': DrugsFilterForm}
    data = {'html': render_to_string(template, context, request)}
    if request.method == 'POST':
        filter_form = DrugsFilterForm(request.POST)
        if filter_form.is_valid():
            updated_drugs = Drugs.objects.filter(created_by=request.user, name__icontains=filter_form.cleaned_data['name'])
            if len(updated_drugs) > 0:
                context['drugs'] = updated_drugs
                data = {'updated_html': render_to_string(template, context, request)}
    return JsonResponse(data)


def create_drug(request):
    drugs_form = DrugsForm
    template = 'settings/create_drug.html'
    context = {'form': drugs_form}
    data = {'html': render_to_string(template, context, request)}
    if request.method == 'POST':
        drugs_form = DrugsForm(request.POST)
        if drugs_form.is_valid():
            try:
                drug = drugs_form.save(commit=False)
                drug.created_by = request.user
                drug.save()
                drugs_list = Drugs.objects.filter(created_by=request.user)
                context = {'drugs': drugs_list, 'form': DrugsFilterForm}
                data = {'updated_html': render_to_string('settings/drugs_list.html', context, request), 'updated_drugs_list':render_to_string('appointments/partial_drugs_selection.html', {'drugs': drugs_list}, request)}
            except IntegrityError:
                context['error'] = 'Drug already listed'
                data = {'html': render_to_string(template, context, request)}
    return JsonResponse(data)


def drug_details(request, pk):
    drug = Drugs.objects.get(pk=pk)
    template = 'settings/drug_details.html'
    context = {'drug': drug}
    data = {'html': render_to_string(template, context, request)}
    return JsonResponse(data)


def update_drug(request, pk):
    drug = Drugs.objects.get(pk=pk)
    drug_form = DrugsForm(request.POST or None, instance=drug)
    template = 'settings/update_drug.html'
    context = {'drug': drug, 'form': drug_form}
    data = {'html': render_to_string(template, context, request)}
    if request.method == 'POST':
        drug = DrugsForm(request.POST or None, instance=drug)
        if drug_form.is_valid():
            try:
                drug.save(commit=False)
                drug.created_by = request.user
                drug.save()
                drugs_list = Drugs.objects.filter(created_by=request.user)
                context = {'drugs': drugs_list, 'form': DrugsFilterForm}
                data = {'updated_html': render_to_string('settings/drugs_list.html', context, request)}
            except IntegrityError:
                context['error'] = 'Drug already listed'
                data = {'html': render_to_string('settings/drugs_list.html', context, request)}
    return JsonResponse(data)


def delete_drug(request, pk):
    drug = Drugs.objects.get(pk=pk)
    template = 'settings/delete_drug.html'
    context = {'drug': drug}
    data = {'html': render_to_string(template, context, request)}
    if request.method == 'POST':
        drug.delete()
        drugs_list = Drugs.objects.filter(created_by=request.user)
        context = {'drugs': drugs_list, 'form': DrugsFilterForm}
        data = {'updated_html': render_to_string('settings/drugs_list.html', context, request)}
    return JsonResponse(data)




