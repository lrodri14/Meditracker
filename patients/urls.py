from django.urls import path
from .views import *
# This views.py file contains all the urls necessary to route all the views, it is composed of 5 routes.

app_name = 'patients'
urlpatterns = [
    path('', patients, name='patients'),
    path('add_patient/', add_patient, name='add_patient'),
    path('details/<int:pk>', patient_details, name='patients_details'),
    path('update/<int:pk>', patient_update, name='patients_update'),
    path('delete/<int:pk>', patient_delete, name='patients_delete'),
]
