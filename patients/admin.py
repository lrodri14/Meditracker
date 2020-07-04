from django.contrib import admin
from .models import Patient, InsuranceCarrier, InsuranceInformation, Allergies, AllergiesInformation, Antecedents

# Register your models here.
admin.site.register(Patient)
admin.site.register(InsuranceCarrier)
admin.site.register(InsuranceInformation)
admin.site.register(Allergies)
admin.site.register(AllergiesInformation)
admin.site.register(Antecedents)
