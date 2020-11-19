from django import forms
from .models import Providers, Visitor

# Your forms go here.


class ProvidersForm(forms.ModelForm):
    class Meta:
        model = Providers
        exclude = ('created_by',)


class ProvidersFilterForm(forms.Form):
    company = forms.CharField(widget=forms.widgets.TextInput)


class VisitorsForm(forms.ModelForm):
    class Meta:
        model = Visitor
        exclude = ('created_by',)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        if user:
            self.fields['company'].queryset = Providers.objects.filter(created_by=user)


class VisitorsFilterForm(forms.Form):
    name = forms.CharField(widget=forms.widgets.TextInput)