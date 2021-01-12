from django.contrib import admin
from .models import CustomUser, UsersProfile, MailingCredential, ContactRequest
from .forms import UserChangeForm, UserCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = BaseUserAdmin.fieldsets + (('Title Info', {'fields': ('roll', 'speciality')}),)
    add_fieldsets = ((None, {'fields': ('username', 'password1', 'password2', 'roll', 'speciality'), }, ), )


admin.site.register(CustomUser, UserAdmin)
admin.site.register(UsersProfile)
admin.site.register(MailingCredential)
admin.site.register(ContactRequest)