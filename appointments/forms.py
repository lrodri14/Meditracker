from .models import Consults
from django import forms


class ConsultsForm(forms.ModelForm):
    date = forms.DateField(widget=forms.SelectDateWidget)
    time = forms.TimeField(widget=forms.TimeInput)
    motive = forms.Textarea(attrs={'cols': 30, 'rows': 4})
    suffering = forms.Textarea(attrs={'cols': 30, 'rows': 4})

    class Meta:
        model = Consults
        exclude = ('created_by',)
