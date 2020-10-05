from .models import Consults, MedicalExams, Drugs
from django import forms
from django.forms import modelformset_factory
from django.utils import timezone
from dateutil import relativedelta
from patients.models import Patient
from django.core.exceptions import ValidationError


class ConsultsForm(forms.ModelForm):
    datetime = forms.DateTimeField(input_formats=['%Y-%m-%dT%H:%M'], widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'), initial=timezone.localtime(timezone.now()))

    class Meta:
        model = Consults
        fields = ('patient', 'datetime', 'motive', 'suffering',)

    def __init__(self, user, *args, **kwargs):
        super(ConsultsForm, self).__init__(*args, **kwargs)
        self.fields['patient'].queryset = Patient.objects.filter(created_by=user)


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

    def __init__(self, user, *args, **kwargs):
        super(UpdateConsultsForm, self).__init__(*args, **kwargs)
        self.fields['drugs'].queryset = Drugs.objects.filter(created_by=user)


class MedicalExamsForm(forms.ModelForm):
    class Meta:
        model = MedicalExams
        fields = ('type', 'image',)

    def clean(self):
        cleaned_data = super().clean()
        type = cleaned_data.get('type')
        image = cleaned_data.get('image')

        if type and not image or image and not type:
            raise ValidationError('You did not fill your exams correctly. "Type" & "Image" must be provided.')


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


class DrugsForm(forms.ModelForm):

    class Meta:
        model = Drugs
        exclude = ('created_by',)






class DrugsFilterForm(forms.ModelForm):
    class Meta:
        model = Drugs
        exclude = ('created_by',)



