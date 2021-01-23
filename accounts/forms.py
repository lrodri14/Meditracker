from django import forms
from django.contrib.auth.forms import UserCreationForm as CreationForm
from django.contrib.auth.forms import UserChangeForm as ChangeForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import CustomUser, UsersProfile, MailingCredential
from PIL import Image, ExifTags
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
    birth_date = forms.DateField(widget=forms.SelectDateWidget(years=[x for x in range(1920, 2101)]), required=None)
    tzone = forms.ChoiceField(choices=[(x, x) for x in pytz.common_timezones])

    class Meta:
        model = UsersProfile
        exclude = ('user', 'profile_pic', 'background_pic', 'contacts')
        widgets = {
            'address': forms.widgets.Textarea(attrs={'rows': 1, 'wrap': 'off'})
        }


class ProfilePictureForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = UsersProfile
        fields = ('profile_pic',)

    def save(self, *args, **kwargs):
        profile_picture = super().save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        width = self.cleaned_data.get('width')
        height = self.cleaned_data.get('height')

        if x < 1:
            x = 1
        if y < 1:
            y = 1

        image = Image.open(profile_picture.profile_pic)
        try:
            exif = dict((ExifTags.TAGS[k], v) for k, v in image._getexif().items() if k in ExifTags.TAGS)
            if exif.get('Orientation') == 6:
                image = image.rotate(270, expand=True)
        except AttributeError:
            pass
        image = image.crop((x, y, width + x, height + y))
        image.save(profile_picture.profile_pic.path, quality=120)

        return profile_picture


class ProfileBackgroundForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.widgets.HiddenInput())
    y = forms.FloatField(widget=forms.widgets.HiddenInput())
    width = forms.FloatField(widget=forms.widgets.HiddenInput())
    height = forms.FloatField(widget=forms.widgets.HiddenInput())

    class Meta:
        model = UsersProfile
        fields = ('background_pic',)

    def save(self, *args, **kwargs):
        background_image = super().save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        width = self.cleaned_data.get('width')
        height = self.cleaned_data.get('height')

        image = Image.open(background_image.background_pic)
        try:
            exif = dict((ExifTags.TAGS[k], v) for k, v in image._getexif().items() if k in ExifTags.TAGS)
            if exif.get('Orientation') == 6:
                image = image.rotate(270, expand=True)
            elif exif.get('Orientation') == 8:
                image = image.rotate(90, expand=True)
        except AttributeError:
            pass
        cropped_image = image.crop((x, y, x + width, y + height))
        cropped_image.save(background_image.background_pic.path)

        return background_image


class MailingCredentialForm(forms.ModelForm):
    class Meta:
        model = MailingCredential
        exclude = ('user',)
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }


class ChatForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={'cols': 35, 'rows': 2, 'placeholder': 'Send Message...'}))





