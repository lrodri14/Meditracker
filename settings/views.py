from django.shortcuts import render, redirect, reverse
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.apps import apps
from patients import forms
from appointments.forms import DrugsForm
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
    insurances_list = InsuranceCarrier.objects.filter(country=request.user.profile.origin)
    template = 'settings/insurance_list.html'
    context = {'insurances': insurances_list}
    return render(request, template, context)


def add_insurance_carrier(request):
    insurance_carrier_form = forms.InsuranceCarrierForm
    context = {'insurance_carrier_form': insurance_carrier_form}
    template = 'settings/insurance_add.html'
    if request.method == 'POST':
        insurance_form = forms.InsuranceCarrierForm(request.POST)
        if insurance_form.is_valid():
            try:
                insurance_form.save()
            except IntegrityError:
                context['unique_error'] = '*This company is already registered for this region.'
                return render(request, template, context)
            else:
                return redirect(reverse('settings:settings'))
    return render(request, template, context)


def insurance_details(request, pk):
    carrier = InsuranceCarrier.objects.get(pk=pk)
    template = 'settings/insurance_details.html'
    context = {'insurance': carrier}
    return render(request, template, context)


def insurance_update(request, pk):
    carrier = InsuranceCarrier.objects.get(pk=pk)
    insurance_form = forms.InsuranceCarrierForm(request.POST, instance=carrier)
    template = 'settings/insurance_update.html'
    context = {'insurance': insurance_form}
    if request.method == 'POST':
        if insurance_form.is_valid():
            try:
                insurance_form.save()
                return redirect(reverse('settings:settings'))
            except IntegrityError:
                context['unique_error'] = '*This company is already registered in your location.'
                return render(request, template, context)
    return render(request, template, context)


def insurance_delete(request, pk):
    try:
        carrier = InsuranceCarrier.objects.get(pk=pk)
        context = {'insurance': carrier}
        template = 'settings/insurance_delete.html'
        if request.method == 'POST':
            if request.POST['choice'] == 'yes':
                carrier.delete()
                return redirect(reverse('settings:settings'))
            else:
                return redirect(reverse('settings:settings'))
        return render(request, template, context)
    except ObjectDoesNotExist:
        return redirect(reverse('settings:settings'))


# Allergies

def allergies_list(request):
    allergies_created = Allergies.objects.filter(created_by=request.user)
    template = 'settings/allergies_list.html'
    context = {'allergies': allergies_created}
    return render(request, template, context)


def allergies_create(request):
    allergies_form = forms.AllergiesForm
    template = 'settings/add_allergies.html'
    context = {'allergies_form': allergies_form}
    if request.method == 'POST':
        allergies_form = forms.AllergiesForm(request.POST)
        if allergies_form.is_valid():
            try:
                allergy = allergies_form.save(commit=False)
                allergy.created_by = request.user
                allergy.save()
                return redirect(reverse('settings:settings'))
            except IntegrityError:
                context['unique_error'] = 'This allergy is already in your options'
                return render(request, template, context)
    return render(request, template, context)


def allergies_details(request, pk):
    allergy = Allergies.objects.get(pk=pk)
    template = 'settings/allergy_details.html'
    context = {'allergy': allergy}
    return render(request, template, context)


def allergies_update(request, pk):
    allergy = Allergies.objects.get(pk=pk)
    template = 'settings/update_allergy.html'
    allergy_form = forms.AllergiesForm(request.POST, instance=allergy)
    context = {'allergy': allergy, 'allergy_form': allergy_form}
    if request.method == 'POST':
        if allergy_form.is_valid():
            try:
                allergy_form.save()
                return redirect(reverse('settings:allergies_list'))
            except IntegrityError:
                context['unique_error'] = 'This allergy is already in your options'
                return render(request, template, context)
    return render(request, template, context)


def allergies_delete(request, pk):
    try:
        allergy = Allergies.objects.get(pk=pk)
        template = 'settings/allergy_delete.html'
        context = {'allergy': allergy}
        if request.method == 'POST':
            if request.POST['choice'] == 'yes':
                allergy.delete()
                return redirect(reverse('settings:settings'))
            else:
                return redirect(reverse('settings:settings'))
        return render(request, template, context)
    except ObjectDoesNotExist:
        return redirect(reverse('settings:settings'))


# Drugs


def drugs_list(request):
    drugs_list = Drugs.objects.filter(created_by=request.user)
    template = 'settings/drugs_list.html'
    context = {'drugs': drugs_list}
    return render(request, template, context)


def create_drug(request):
    drugs_form = DrugsForm
    template = 'settings/create_drug.html'
    context = {'form': drugs_form}
    if request.method == 'POST':
        drugs_form = DrugsForm(request.POST)
        if drugs_form.is_valid():
            drug = drugs_form.save(commit=False)
            drug.created_by = request.user
            drug.save()
            return redirect(reverse('settings:settings'))
    return render(request, template, context)


def drug_details(request, pk):
    drug = Drugs.objects.get(pk=pk)
    template = 'settings/drug_details.html'
    context = {'drug': drug}
    return render(request, template, context)


def update_drug(request, pk):
    drug = Drugs.objects.get(pk=pk)
    drug_form = DrugsForm(request.POST or None, instance=drug)
    template = 'settings/update_drug.html'
    context = {'drug': drug, 'form': drug_form}
    if request.POST:
        if drug_form.is_valid():
            drug_form.save()
    return render(request, template, context)


def delete_drug(request, pk):
    try:
        drug = Drugs.objects.get(pk=pk)
        template = 'settings/delete_drug.html'
        context = {'drug': drug}
        if request.method == 'POST':
            if request.POST['choice'] == 'yes':
                drug.delete()
                return redirect(reverse('settings:settings'))
            else:
                return redirect(reverse('settings:settings'))
        return render(request, template, context)
    except ObjectDoesNotExist:
        return redirect(reverse('settings:settings'))



