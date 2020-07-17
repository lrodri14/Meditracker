from django.urls import path
from .views import *

app_name = 'appointments'
urlpatterns = [
    path('', consults, name='consults'),
    path('consults_list', consults_list, name='consults_list'),
    path('create_consult', create_consult, name='create_consult'),
    path('consult_details/<int:pk>', consults_details, name='consult_details'),
    path('update_consult/<int:pk>', update_consult, name='update_consult'),
    path('delete_consult/<int:pk>', delete_consult, name='delete_consult'),
    path('consult_register/', consults_register, name='consult_register'),
    path('consult_date_update/<int:pk>', consult_date_update, name='consult_date_update'),
    path('consult_cancel/<int:pk>', consult_cancel, name='consult_cancel'),
]
