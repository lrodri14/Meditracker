from django import forms
from patients.models import InsuranceCarrier


class InsuranceForm(forms.ModelForm):
    class Meta:
        Model = InsuranceCarrier
        fields = ['company']
