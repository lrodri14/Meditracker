from django.urls import path
from .views import *

app_name = 'patients'
urlpatterns = [
    path('', patients, name='patients'),
    path('add_patient/', add_patient, name='add_patient'),
]
