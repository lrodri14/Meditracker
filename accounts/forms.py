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


class DoctorSignUpForm(CreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'speciality')
        widgets = {
            'email': forms.widgets.EmailInput(),
            'speciality': forms.widgets.Select()
        }

    def __init__(self, *args, **kwargs):
        super(DoctorSignUpForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['speciality'].required = True


class AssistantSignUpForm(CreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'email': forms.widgets.EmailInput(),
        }

    def __init__(self, *args, **kwargs):
        super(AssistantSignUpForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True


class ProfileForm(forms.ModelForm):
    profile_pic = forms.ImageField(widget=forms.FileInput, required=None)
    birth_date = forms.DateField(widget=forms.SelectDateWidget(years=[x for x in range(1920, 2101)]), required=None)
    tzone = forms.ChoiceField(choices=[(x, x) for x in pytz.common_timezones])

    class Meta:
        model = UsersProfile
        exclude = ('user',)
        widgets = {
            'address': forms.widgets.Textarea(attrs={'rows': 1, 'cols': 80, 'wrap': 'off'})
        }



