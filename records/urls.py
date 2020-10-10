from django.urls import path
from .views import *

app_name = 'records'
urlpatterns = [
    path('records_list/', records_list, name='records_list'),
    path('records_list/<int:pk>', records_list, name='records_list'),
]