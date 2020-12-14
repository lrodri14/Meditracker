"""
    This views.py file contains all the urls necessary to route all the views, it is composed of 5 routes.
"""

# Imports
from django.urls import path
from .views import *

app_name = 'patients'
urlpatterns = [
    path('', patients, name='patients'),
    path('filter_patients', filter_patients, name='filter_patients'),
    path('add_patient/', add_patient, name='add_patient'),
    path('details/<int:pk>', patient_details, name='patients_details'),
    path('update/<int:pk>', update_patient, name='update_patient'),
    path('delete/<int:pk>', delete_patient, name='delete_patient'),
]
