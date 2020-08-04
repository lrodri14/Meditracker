from django import forms
from django.contrib.auth.forms import UserCreationForm as CreationForm
from django.contrib.auth.forms import UserChangeForm as ChangeForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import CustomUser, UsersProfile
import pytz


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

    def clean(self):
        cleaned_data = super().clean()
        roll = cleaned_data.get('roll')
        speciality = cleaned_data.get('speciality')

        if roll == 'Doctor' and speciality == '':
            msg = 'You must specify your area'
            self.add_error('speciality', msg)



class ProfileForm(forms.ModelForm):
    profile_pic = forms.ImageField(widget=forms.FileInput, required=None)
    birth_date = forms.DateField(widget=forms.SelectDateWidget(years=[x for x in range(1920, 2101)]), required=None)
    tzone = forms.ChoiceField(choices=[(x, x) for x in pytz.common_timezones])

    class Meta:
        model = UsersProfile
        exclude = ('user',)



