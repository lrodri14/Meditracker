# Imports
from .models import *
from django import forms
from django.core.exceptions import ValidationError
from django.forms import modelformset_factory, inlineformset_factory

# List containing all the available years
years = [years for years in range(1920, 2101)]

# This forms.py file contains all the forms needed to operate CRUD functionality in the Patient App.
# It contains 9 forms, and is separated in 4 sections: Patient, Allergies, Insurance, Antecedents forms.

# Patients Forms
# #################################


class PatientForm(forms.ModelForm):
    """
        DOCSTRING:
        The PatientForm form inherits form the forms.ModelForm class, and it is used to create
        Patient instances, the birthday field is been set the forms.selectDateWidget widget.
    """

    birthday = forms.DateField(widget=forms.SelectDateWidget(years=years))

    class Meta:
        model = Patient
        exclude = ('created_by',)


class PatientFilter(forms.Form):
    """
        DOCSTRING:
        The PatientFilter form inherits form the forms.Form class, and it is used to filter Patient
        data from the server side.
    """
    patient = forms.CharField(widget=forms.TextInput)


# Insurance Forms
# #################################


class InsuranceCarrierForm(forms.ModelForm):
    """
        DOCSTRING:
        The InsuranceCarrierForm form inherits form the forms.ModelForm class, and it is used to create
        InsuranceCarrierInstances instances.
    """
    class Meta:
        model = InsuranceCarrier
        exclude = ('created_by',)


class InsuranceCarrierFilterForm(forms.ModelForm):
    """
        REPAIR
        DOCSTRING:
        The InsuranceCarrierFilterForm form inherits form the forms.Form class, and it is used to filter InsuranceCarrier
        data from the server side.
    """
    class Meta:
        model = InsuranceCarrier
        exclude = ('country', 'created_by')


class InsuranceInformationForm(forms.ModelForm):
    """
        DOCSTRING:
        The InsuranceInformationForm form inherits form the forms.ModelForm class, and it is used to create
        InsuranceInformationForm instances, the expiration_date field is been set the forms.selectDateWidget widget.
        The clean method has been overwritten in this form to secure that if an instance is to be created, it should
        contain all the data, else an error will be raised.
    """
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


# Allergies Forms
# #################################


class AllergiesForm(forms.ModelForm):
    """
        DOCSTRING:
        The AllergiesForm form inherits form the forms.ModelForm class, and it is used to create
        AllergiesForm instances.
    """
    class Meta:
        model = Allergies
        exclude = ('created_by',)


class AllergiesFilterForm(forms.ModelForm):
    """
        DOCSTRING:
        The AllergiesFilterForm form inherits form the forms.ModelForm class, and it is used to filter Allergies
        data from the server side.
    """
    class Meta:
        model = Allergies
        exclude = ('created_by',)


class AllergiesInformationForm(forms.ModelForm):
    """
        DOCSTRING:
        The AllergiesInformationForm form inherits form the forms.ModelForm class, and it is used to create
        AllergiesInformation instances, the about field is been set the forms.Textarea widget and set the rows
        and columns attributes to 2. The clean method has been overwritten in this form to secure that if an instance
        is to be created, it should contain all the data, else an error will be raised. Two Formsets have been created
        from this form, the AllergiesInformationFormset to create as many instances as needed once, and the
        AllergiesInformationUpdateFormset to update as many instances as needed.
    """
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


# Antecedents Forms
# #################################


class AntecedentForm(forms.ModelForm):
    """
        DOCSTRING:
        The AntecedentForm form inherits form the forms.ModelForm class, and it is used to create
        Antecedent instances, the info field is been set the forms.Textarea widget and set the rows
        and columns attributes to 2. The clean method has been overwritten in this form to secure that if an instance
        is to be created, it should contain all the data, else an error will be raised. Two Formsets have been created
        from this form, the AntecedentFormset to create as many instances as needed once, and the
         AntecedentUpdateFormset to update as many instances as needed.
    """
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

