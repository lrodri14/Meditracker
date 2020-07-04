from django import forms
from .models import *


class PatientForm(forms.ModelForm):
    birthday = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Patient
        exclude = ('age',)


class InsuranceCarrierForm(forms.ModelForm):

    class Meta:
        model = InsuranceCarrier
        fields = '__all__'


class InsuranceInformationForm(forms.ModelForm):
    expiration_date = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = InsuranceInformation
        exclude = ('patient',)


class Allergies(forms.ModelForm):

    class Meta:
        model = Allergies
        fields = '__all__'


class AllergiesInformationForm(forms.ModelForm):

    class Meta:
        model = AllergiesInformation
        exclude = ('patient',)


class AntecedentForm(forms.ModelForm):
    class Meta:
        model = Antecedents
        exclude = ('patient',)
