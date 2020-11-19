from django.core.exceptions import ValidationError
from .models import Consults, MedicalExams, Drugs
from django import forms
from django.forms import modelformset_factory
from django.utils import timezone
from dateutil import relativedelta
from patients.models import Patient


class ConsultsForm(forms.ModelForm):
    datetime = forms.DateTimeField(input_formats=['%Y-%m-%dT%H:%M'], widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'), initial=timezone.localtime(timezone.now()))

    class Meta:
        model = Consults
        fields = ('patient', 'datetime', 'motive', 'suffering',)
        widgets = {
            'motive': forms.Textarea(attrs={'rows': 8, 'columns': 5}),
            'suffering': forms.Textarea(attrs={'rows': 8, 'columns': 5})
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ConsultsForm, self).__init__(*args, **kwargs)
        self.fields['patient'].queryset = Patient.objects.filter(created_by=self.user)

    def clean(self):
        cleaned_data = super().clean()
        datetime = cleaned_data.get('datetime')
        if datetime.date() < timezone.localtime().date():
            raise ValidationError('Unable to create a consult for this date.', code='invalid_date')
        return cleaned_data


class UpdateConsultsForm(forms.ModelForm):
    class Meta:
        model = Consults
        exclude = ('patient', 'datetime', 'motive', 'suffering', 'created_by', 'status', 'medical_status')
        widgets = {
            'charge': forms.NumberInput(attrs={'placeholder': '0.00'}),
            'digestive_system': forms.Textarea(attrs={'rows': 2, 'cols': 70}),
            'endocrine_system': forms.Textarea(attrs={'rows': 2, 'cols': 70}),
            'lymphatic_system': forms.Textarea(attrs={'rows': 2, 'cols': 70}),
            'respiratory_system': forms.Textarea(attrs={'rows': 2, 'cols': 70}),
            'renal_system': forms.Textarea(attrs={'rows': 2, 'cols': 70}),
            'head_exploration': forms.Textarea(attrs={'rows': 2, 'cols': 70}),
            'thorax_exploration': forms.Textarea(attrs={'rows': 2, 'cols': 70}),
            'cie_10_detail': forms.Textarea(attrs={'rows': 2, 'cols': 150}),
            'diagnose': forms.Textarea(attrs={'rows': 2, 'cols': 150}),
            'procedure': forms.Textarea(attrs={'rows': 2, 'cols': 150}),
            'analysis': forms.Textarea(attrs={'rows': 2, 'cols': 150}),
            'notes': forms.Textarea(attrs={'rows': 2, 'cols': 150}),
            'drugs': forms.CheckboxSelectMultiple(),
            'medicine': forms.Textarea(attrs={'rows': 5, 'cols': 10, 'placeholder': 'Indications Here'}),
            'actions': forms.Textarea(attrs={'rows': 5, 'cols': 10, 'placeholder': 'Extra Considerations'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(UpdateConsultsForm, self).__init__(*args, **kwargs)
        self.fields['drugs'].queryset = Drugs.objects.filter(created_by=user)

    def clean(self):
        cleaned_data = super().clean()
        cie_group = cleaned_data.get('cie_10_group')
        cie_detail = cleaned_data.get('cie_10_detail')
        if (cie_group and not cie_detail) or (cie_detail and not cie_group):
            raise ValidationError("CIE-10 diagnose details are not completed.", code='invalid_cie_10_details')
        return cleaned_data


class MedicalExamsForm(forms.ModelForm):
    class Meta:
        model = MedicalExams
        fields = ('type', 'image',)

    def clean(self):
        cleaned_data = super().clean()
        exam_type = cleaned_data.get('type')
        image = cleaned_data.get('image')

        if (exam_type and not image) or (image and not exam_type):
            raise ValidationError("'Type' and 'Image', both must be provided in your exams.", code='invalid_exams')
        return cleaned_data


MedicalExamsFormset = modelformset_factory(model=MedicalExams, form=MedicalExamsForm, can_delete=True)


years = [y for y in range(1920, timezone.now().year+1)]


class RecordsDateFilterForm(forms.Form):
    date_from = forms.DateField(widget=forms.SelectDateWidget(years=years), initial=timezone.now() - relativedelta.relativedelta(month=3))
    date_to = forms.DateField(widget=forms.SelectDateWidget(years=years), initial=timezone.now())


class AgendaDateFilterForm(forms.Form):
    date_from = forms.DateField(widget=forms.SelectDateWidget(years=years), initial=timezone.now())
    date_to = forms.DateField(widget=forms.SelectDateWidget(years=years), initial=timezone.now())


class ConsultsDetailsFilterForm(forms.Form):
    date_from = forms.DateField(widget=forms.SelectDateWidget(years=years), initial=timezone.now())
    date_to = forms.DateField(widget=forms.SelectDateWidget(years=years), initial=timezone.now())


MONTH_CHOICES = (
    (0, '-------'),
    (1, 'January'),
    (2, 'February'),
    (3, 'March'),
    (4, 'April'),
    (5, 'May'),
    (6, 'June'),
    (7, 'July'),
    (8, 'August'),
    (9, 'September'),
    (10, 'October'),
    (11, 'November'),
    (12, 'December'),
)

YEARS_CHOICES = (
    (i, i) for i in range(1920, timezone.now().year+2)
)


class RegistersFilter(forms.Form):
    patient = forms.CharField(max_length=100, widget=forms.TextInput,required=False)
    month = forms.ChoiceField(choices=MONTH_CHOICES, required=False)
    year = forms.ChoiceField(choices=YEARS_CHOICES, required=False)


class DrugCategoryFilterForm(forms.Form):

    CATEGORY_CHOICES = (
        ('', '---------'),
        ('AP', 'Antipyretics'),
        ('AG', 'Analgesics'),
        ('AM', 'Antimalarial'),
        ('AB', 'Antibiotics'),
        ('AS', 'Antiseptics'),
        ('MS', 'Mood Stabilizers'),
        ('HR', 'Hormone Replacement'),
        ('OC', 'Oral Contraceptives'),
        ('S', 'Stimulants'),
        ('T', 'Tranquilizers'),
        ('ST', 'Statins'),

    )

    category = forms.CharField(max_length=50,  widget=forms.Select(choices=CATEGORY_CHOICES))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].required = False


class DrugsForm(forms.ModelForm):

    class Meta:
        model = Drugs
        exclude = ('created_by',)


class DrugsFilterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].required = False

    class Meta:
        model = Drugs
        exclude = ('created_by',)



