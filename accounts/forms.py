from django import forms
from django.contrib.auth.forms import UserCreationForm as CreationForm
from django.contrib.auth.forms import UserChangeForm as ChangeForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import User
from .models import CustomUser


class UserCreationForm(CreationForm):
    class Meta(CreationForm.Meta):
        model = CustomUser


class UserChangeForm(ChangeForm):
    password = ReadOnlyPasswordHashField

    class Meta(ChangeForm.Meta):
        model = CustomUser


class SignUpForm(CreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField()
    roll = forms.Select()
    speciality = forms.Select()

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'roll', 'speciality')



