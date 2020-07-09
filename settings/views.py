from django.shortcuts import render, redirect, reverse
from django.db import IntegrityError
from django.apps import apps
from patients import forms
InsuranceCarrier = apps.get_model('patients', 'InsuranceCarrier')
Allergies = apps.get_model('patients', 'Allergies')

# Create your views here.


def settings(request):
    template = 'settings/settings.html'
    insurances_list = InsuranceCarrier.objects.filter(country=request.user.profile.origin)
    allergies_created_list = Allergies.objects.all()
    context = {'insurance_list': insurances_list, 'allergies_list': allergies_created_list}
    return render(request, template, context)


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


def allergies_list(request):
    pass


def allergies_create(request):
    pass


def allergies_delete(request):
    pass


def allergies_update(request):
    pass



