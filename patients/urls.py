from django.urls import path
from .views import *

app_name = 'patients'
urlpatterns = [
    path('', patients, name='patients'),
    path('add_patient/', add_patient, name='add_patient'),
    path('details/<int:pk>', patient_details, name='patients_details'),
    path('delete/<int:pk>', patient_delete, name='patients_delete'),
    path('update/<int:pk>', patient_update, name='patients_update'),
]
