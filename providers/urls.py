from django.urls import path
from .views import *

app_name = 'providers'
urlpatterns = [
    path('', providers, name='providers'),
    path('providers_list', providers_list, name='providers_list'),
    path('providers_filter', filter_providers_list, name='providers_filter'),
    path('create_provider', create_providers, name='create_provider'),
    path('provider_details/<int:pk>', providers_details, name='provider_details'),
    path('update_provider/<int:pk>', update_providers, name='update_provider'),
    path('delete_provider/<int:pk>', delete_provider, name='delete_provider'),
    path('visitors', visitors_list, name='visitors'),
    path('visitors_filter', filter_visitors_list, name='visitors_filter'),
    path('create_visitor', create_visitor, name='create_visitor'),
    path('visitor_details/<int:pk>', visitors_details, name='visitor_details'),
    path('update_visitor/<int:pk>', update_visitors, name='update_visitors'),
    path('delete_visitor/<int:pk>', delete_visitor, name='delete_visitor'),
]