from django.contrib import admin
from .models import Patient, InsuranceCarrier, InsuranceInformation, Allergy, AllergyInformation, Antecedent

# Register your models here.
admin.site.register(Patient)
admin.site.register(InsuranceCarrier)
admin.site.register(InsuranceInformation)
admin.site.register(Allergy)
admin.site.register(AllergyInformation)
admin.site.register(Antecedent)
