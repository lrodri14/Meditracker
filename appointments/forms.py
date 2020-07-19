from .models import Consults
from django import forms
from django.utils import timezone
import datetime
from dateutil import relativedelta


class ConsultsForm(forms.ModelForm):
    datetime = forms.DateTimeField(input_formats=['%Y-%m-%dT%H:%M'], widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'))

    class Meta:
        model = Consults
        fields = ('patient', 'datetime', 'motive', 'suffering',)


class UpdateConsultsForm(forms.ModelForm):

    class Meta:
        model = Consults
        exclude = ('patient', 'datetime', 'motive', 'suffering', 'created_by', 'status', 'created_at')
        widgets = {
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
            'medicine': forms.Textarea(attrs={'rows': 5, 'cols': 150}),
            'actions': forms.Textarea(attrs={'rows': 2, 'cols': 150}),
        }


years = [y for y in range(1920, timezone.now().year+1)]


class DateFilterForm(forms.Form):
    date_from = forms.DateField(widget=forms.SelectDateWidget(years=years), initial=timezone.now() - relativedelta.relativedelta(month=3))
    date_to = forms.DateField(widget=forms.SelectDateWidget(years=years), initial=timezone.now())
