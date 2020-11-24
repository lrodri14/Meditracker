from django.urls import path
from .views import *

app_name = 'records'
urlpatterns = [
    path('records_list/', records_list, name='records_list'),
    path('filtered_records/<int:pk>', filtered_records, name='filtered_records')
]