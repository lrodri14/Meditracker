from django.contrib import admin
from .models import Consults, Cie10Group, Drugs, MedicalExams
# Register your models here.

admin.site.register(Consults)
admin.site.register(Cie10Group)
admin.site.register(Drugs)
admin.site.register(MedicalExams)
