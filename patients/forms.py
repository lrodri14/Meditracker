from django import forms
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
    # insurance_carrier = forms.ModelChoiceField(queryset=InsuranceCarrier.objects.filter())
    expiration_date = forms.DateField(widget=forms.SelectDateWidget(years=years))

    class Meta:
        model = InsuranceInformation
        exclude = ('patient',)


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
            self._errors['Allergies'] = self.error_class(["Both 'Type' and 'About' fields must be provided."])
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
            self._errors['Antecedents'] = self.error_class(["Both 'Antecedent' and 'Info' fields must be provided."])
        return cleaned_data


AntecedentFormset = modelformset_factory(model=Antecedents, form=AntecedentForm, can_delete=True)
AntecedentUpdateFormset = inlineformset_factory(parent_model=Patient, model=Antecedents, form=AntecedentForm, can_delete=True, extra=1)

