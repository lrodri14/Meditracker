from django.urls import path
from .views import *

app_name = 'settings'
urlpatterns = [
    path('', settings, name='settings'),
    path('insurance_list', insurance_list, name='insurance_list'),
    path('insurance_add/', add_insurance_carrier, name='insurance_add'),
    path('insurance_details/<int:pk>', insurance_details, name='insurance_details'),
    path('update_insurance/<int:pk>', insurance_update, name='insurance_update'),
    path('insurance_delete/<int:pk>', insurance_delete, name='insurance_delete'),
    path('allergy_list', allergies_list, name='allergies_list'),
    path('allergy_add/', allergies_create, name='allergy_add'),
    path('allergies_details/<int:pk>', allergies_details, name='allergies_details'),
    path('allergies_update/<int:pk>', allergies_update, name='allergies_update'),
    path('allergies_delete/<int:pk>', allergies_delete, name='allergies_delete'),
    path('drugs_list/', drugs_list, name='drugs_list'),
    path('drug_add/', create_drug, name='drug_add'),
    path('drug_details/<int:pk>', drug_details, name='drug_details'),
    path('update_drug/<int:pk>', update_drug, name='drug_update'),
    path('delete_drug/<int:pk>', delete_drug, name='drug_delete'),
]
