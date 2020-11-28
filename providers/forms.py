"""
    This .py file contains all the forms need for the provider's app to work.
    It is composed of two types of forms: Creation Forms and Filtering Forms.
"""

from django import forms
from .models import Providers, Visitor

# Creation Forms


class ProvidersForm(forms.ModelForm):
    """
        DOCSTRING:
        This ProvidersForm class inherits from the forms.ModelForm class
        and it is used to create providers in our providers app.
    """
    class Meta:
        model = Providers
        exclude = ('created_by',)


class VisitorsForm(forms.ModelForm):
    """
        DOCSTRING:
        This VisitorsrsForm class inherits from the forms.ModelForm class
        and it is used to create visitors in our providers app. This class
        also overwrites the __init__ method and receives a key worded argument
        which is the 'user' argument, it is used to filter the selections in the
        'company field' and shows only used related data.
    """
    class Meta:
        model = Visitor
        exclude = ('created_by',)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        if user:
            self.fields['company'].queryset = Providers.objects.filter(created_by=user)


# Filtering Forms


class ProvidersFilterForm(forms.Form):
    """
        DOCSTRING:
        This ProvidersFilterForm is used to retrieve data related to
         providers based on query.
    """
    company = forms.CharField(widget=forms.widgets.TextInput)


class VisitorsFilterForm(forms.Form):
    """
        DOCSTRING:
        This VisitorsFilterForm is used to retrieve data related to
         visitors based on query.
    """
    name = forms.CharField(widget=forms.widgets.TextInput)