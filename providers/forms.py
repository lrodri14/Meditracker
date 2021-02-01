"""
    This .py file contains all the forms need for the provider's app to work.
    It is composed of two types of forms: Creation Forms and Filtering Forms.
"""

from django import forms
from .models import Provider, Visitor
from utilities.global_utilities import ORIGIN_CHOICES

# Creation Forms


class ProviderForm(forms.ModelForm):
    """
        DOCSTRING:
        This ProvidersForm class inherits from the forms.ModelForm class
        and it is used to create providers in our providers app.
    """

    country_code = forms.CharField(widget=forms.Select(choices=ORIGIN_CHOICES))

    class Meta:
        model = Provider
        exclude = ('created_by',)


class VisitorForm(forms.ModelForm):
    """
        DOCSTRING:
        This VisitorsrsForm class inherits from the forms.ModelForm class
        and it is used to create visitors in our providers app. This class
        also overwrites the __init__ method and receives a key worded argument
        which is the 'user' argument, it is used to filter the selections in the
        'company field' and shows only used related data.
    """

    country_code = forms.CharField(widget=forms.Select(choices=ORIGIN_CHOICES))

    class Meta:
        model = Visitor
        exclude = ('created_by',)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        if user:
            self.fields['company'].queryset = Provider.objects.filter(created_by=user)


# Filtering Forms


class ProviderFilterForm(forms.Form):
    """
        DOCSTRING:
        This ProvidersFilterForm is used to retrieve data related to
         providers based on query.
    """
    company = forms.CharField(widget=forms.widgets.TextInput)


class VisitorFilterForm(forms.Form):
    """
        DOCSTRING:
        This VisitorsFilterForm is used to retrieve data related to
        visitors based on query.
    """
    name = forms.CharField(widget=forms.widgets.TextInput)


class EmailForm(forms.Form):
    """
        DOCSTRING:
        This EmailForm is used to retrieve the content of the email
        that will be sent to any of the providers chosen by the user.
        Content such as the: Subject And Email Body
    """

    subject = forms.CharField(widget=forms.TextInput)
    body = forms.CharField(widget=forms.Textarea(attrs={"cols": 100, 'rows': 8}))
