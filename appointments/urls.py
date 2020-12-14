"""
    DOCSTRING:
    This urls.py file contains all the urls needed to route every single view from the .views.py file in this app.
"""

# Imports
from django.urls import path
from .views import *

app_name = 'appointments'
urlpatterns = [
    path('', appointments, name='appointments'),
    path('create_appointment', create_appointment, name='create_appointment'),
    path('consult_details/<int:pk>', consults_details, name='consult_details'),
    path('consult_summary/<int:pk>', consult_summary, name='consult_summary'),
    path('update_consult/<int:pk>', update_consult, name='update_consult'),
    path('cancel_appointment/<int:pk>', cancel_appointment, name='cancel_appointment'),
    path('agenda/', agenda, name='agenda'),
    path('filter_agenda/', filter_agenda, name='filter_agenda'),
    path('registers', registers, name='registers'),
    path('filter_registers', filter_registers, name='filter_registers'),
    path('confirm_appointment/<int:pk>', confirm_appointment, name='confirm_appointment'),
    path('appointment_date_update/<int:pk>', appointment_date_update, name='appointment_date_update'),
]
