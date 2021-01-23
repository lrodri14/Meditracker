"""
    This urls.py file contains all the urls used for the main app to work properly.
"""

from django.urls import path
from .views import main

app_name = 'main'
urlpatterns = [
    path('', main, name='main'),
]