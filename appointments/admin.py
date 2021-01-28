from django.contrib import admin
from .models import Consult, Cie10Group, Drug, MedicalTest, MedicalTestResult
# Register your models here.

admin.site.register(Consult)
admin.site.register(Cie10Group)
admin.site.register(Drug)
admin.site.register(MedicalTest)
admin.site.register(MedicalTestResult)
