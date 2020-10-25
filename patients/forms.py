from gettext import gettext

from django import forms
from django.core.exceptions import ValidationError
from django.forms import modelformset_factory, inlineformset_factory
from .models import *

years = [years for years in range(1920, 2101)]


class PatientForm(forms.ModelForm):
    birthday = forms.DateField(widget=forms.SelectDateWidget(years=years))

    class Meta:
        model = Patient
        exclude = ('created_by',)


class PatientFilter(forms.Form):
    patient = forms.CharField(widget=forms.TextInput)


class InsuranceCarrierForm(forms.ModelForm):

    class Meta:
        model = InsuranceCarrier
        exclude = ('created_by',)


class InsuranceCarrierFilterForm(forms.ModelForm):
    class Meta:
        model = InsuranceCarrier
        exclude = ('country', 'created_by')


class InsuranceInformationForm(forms.ModelForm):
    expiration_date = forms.DateField(widget=forms.SelectDateWidget(years=years))

    class Meta:
        model = InsuranceInformation
        exclude = ('patient',)

    def clean(self):
        cleaned_data = super().clean()
        carrier = cleaned_data.get('insurance_carrier')
        insurance_type = cleaned_data.get('type_of_insurance')
        expiration_date = cleaned_data.get('expiration_date')
        if (carrier and not insurance_type) or (insurance_type and not carrier):
            raise ValidationError("Insurance information incomplete")
        elif (carrier and insurance_type) and (expiration_date <= timezone.localtime().date()):
            raise ValidationError('Insurance has already expired')
        return cleaned_data


class AllergiesForm(forms.ModelForm):

    class Meta:
        model = Allergies
        exclude = ('created_by',)


class AllergiesFilterForm(forms.ModelForm):

    class Meta:
        model = Allergies
        exclude = ('created_by',)


class AllergiesInformationForm(forms.ModelForm):

    class Meta:
        model = AllergiesInformation
        exclude = ('patient',)
        widgets = {
            'about': forms.widgets.Textarea(attrs={'rows': 2, 'columns': 2})
        }

    def clean(self):
        cleaned_data = super().clean()
        allergy_type = cleaned_data.get('allergy_type')
        about = cleaned_data.get('about')
        if (allergy_type and not about) or (about and not allergy_type):
            raise ValidationError("Both 'Type' and 'About' fields must be provided", code='incomplete_data')
        return cleaned_data


AllergiesInformationFormset = modelformset_factory(model=AllergiesInformation, form=AllergiesInformationForm, can_delete=True, extra=1)
AllergiesInformationUpdateFormset = inlineformset_factory(parent_model=Patient, model=AllergiesInformation, form=AllergiesInformationForm, can_delete=True, extra=1)


class AntecedentForm(forms.ModelForm):
    class Meta:
        model = Antecedents
        exclude = ('patient',)
        widgets = {
            'info': forms.widgets.Textarea(attrs={'rows': 2, 'columns': 2})
        }

    def clean(self):
        cleaned_data = super().clean()
        antecedent = cleaned_data.get('antecedent')
        info = cleaned_data.get('info')
        if (antecedent and not info) or (info and not antecedent):
            raise ValidationError("Both 'Antecedent' and 'Info' fields must be provided", code='incomplete_data')
        return cleaned_data


AntecedentFormset = modelformset_factory(model=Antecedents, form=AntecedentForm, can_delete=True)
AntecedentUpdateFormset = inlineformset_factory(parent_model=Patient, model=Antecedents, form=AntecedentForm, can_delete=True, extra=1)

