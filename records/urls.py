"""
    DOCSTRING:
    This urls.py file contains all the urls needed for the records app to route all the views defined.s
"""

# Imports
from django.urls import path
from .views import *

app_name = 'records'
urlpatterns = [
    path('', records, name='records'),
    path('filter_records/', filter_records, name='filter_records'),
    path('personal_records/<int:pk>', personal_records, name='personal_records')
]