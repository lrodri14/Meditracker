from django.urls import path
from .views import *

app_name = 'appointments'
urlpatterns = [
    path('', consults, name='consults'),
    path('consults_list', consults_list, name='consults_list'),
    path('create_consult', create_consult, name='create_consult'),
    path('consult_details', consults_details, name='consult_details'),
    path('update_consult', update_consult, name='update_consult'),
    path('delete_consult', delete_consult, name='delete_consult'),
]