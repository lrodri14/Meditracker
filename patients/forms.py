from django import forms
from .models import *

years = [years for years in range(1920, 2101)]


class PatientForm(forms.ModelForm):
    birthday = forms.DateField(widget=forms.SelectDateWidget(years=years))

    class Meta:
        model = Patient
        exclude = ('created_by',)


class InsuranceCarrierForm(forms.ModelForm):

    class Meta:
        model = InsuranceCarrier
        exclude = ('created_by',)


class InsuranceCarrierFilterForm(forms.ModelForm):
    class Meta:
        model = InsuranceCarrier
        exclude = ('country', 'created_by')


class InsuranceInformationForm(forms.ModelForm):
    # insurance_carrier = forms.ModelChoiceField(queryset=InsuranceCarrier.objects.filter())
    expiration_date = forms.DateField(widget=forms.SelectDateWidget(years=years))

    class Meta:
        model = InsuranceInformation
        exclude = ('patient',)


class AllergiesForm(forms.ModelForm):

    class Meta:
        model = Allergies
        exclude = ('created_by',)


class AllergiesInformationForm(forms.ModelForm):

    class Meta:
        model = AllergiesInformation
        exclude = ('patient',)


class AntecedentForm(forms.ModelForm):
    class Meta:
        model = Antecedents
        exclude = ('patient',)


class PatientFilter(forms.Form):
    patient = forms.CharField(widget=forms.TextInput)
