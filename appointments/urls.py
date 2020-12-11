"""
    DOCSTRING:
    This urls.py file contains all the urls needed to route every single view from the .views.py file in this app.
"""

# Imports
from django.urls import path
from .views import *

app_name = 'appointments'
urlpatterns = [
    path('', consults, name='consults'),
    path('create_consult', create_consult, name='create_consult'),
    path('consult_details/<int:pk>', consults_details, name='consult_details'),
    path('consult_summary/<int:pk>', consult_summary, name='consult_summary'),
    path('update_consult/<int:pk>', update_consult, name='update_consult'),
    path('cancel_consult/<int:pk>', cancel_consult, name='cancel_consult'),
    path('agenda/', agenda, name='agenda'),
    path('filter_agenda/', filter_agenda, name='filter_agenda'),
    path('register', registers, name='registers'),
    path('filter_registers', registers_filter, name='filter_registers'),
    path('consult_confirm/<int:pk>', consult_confirm, name='consult_confirm'),
    path('consult_date_update/<int:pk>', consult_date_update, name='consult_date_update'),
]
