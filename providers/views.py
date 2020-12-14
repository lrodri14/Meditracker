"""
     This views.py contains all the views needed for the Providers App Logic.
     It is separated into two sections 'Providers Related Logic' and 'Visitors Related Logic
"""


# Imports
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse
from django.db import IntegrityError
from django.template.loader import render_to_string
from .models import Provider, Visitor
from .forms import ProviderForm, ProviderFilterForm, VisitorForm, VisitorFilterForm

# Create your views here.
# Providers Related Logic


def providers(request):
    """
        DOCSTRING:
        The providers function is used to display the main page of the providers app,
        it doesn't retrieves any data from the database, it only renders a template,
        it's only parameter is a 'request' which expects a request object.
    """
    template = 'providers/providers.html'
    return render(request, template, context={})


def providers_list(request):
    """
        DOCSTRING:
        The providers_list functions is used to display a list containing all the providers
        retrieved from the database based on a parameter, which we collect from the 'HTTP_PROVIDER_TYPE'
        custom header we receive in our request and extract from the request.META dictionary, it can be
        'LP' for laboratory providers and 'MP' for medical providers, we render this content, as well
        as the filter_form and the requested_type which is the provider_type we extracted from the request.META,
        this for template logic related topics. This data is returned by the function as a JsonResponse Object.
        It only accepts one parameter 'request', which expects a request object.
    """
    requested_type = request.GET.get('provider_type')
    listed_providers = Provider.objects.filter(provider_type=requested_type, created_by=request.user).order_by('company')
    paginator = Paginator(listed_providers, 16)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    filter_form = ProviderFilterForm
    template = 'providers/providers_list.html' if not page else 'providers/providers_partial_list.html'
    context = {'providers': page_obj, 'filter_form': filter_form, 'requested_type': requested_type}
    data = {'html': render_to_string(template, context, request)}
    return JsonResponse(data)


def filter_providers(request):
    """
        DOCSTRING:
        The filter_providers_list function is used to retrieve providers from the database based on a 'query'
        we extract from the 'HTTP_QUERY' custom header and 'provider_type' parameter we extract from the
        'HTTP_PROVIDER_TYPE' custom header, it returns only this content since the template we render is just
        a table row, so there is no need to return the filter_form and the requested_type. It's only parameter
        is 'request' and expects an request object.
    """
    query = request.GET.get('query')
    provider_type = request.GET.get('provider_type')
    filtered_providers = Provider.objects.filter(company__icontains=query, provider_type=provider_type, created_by=request.user).order_by('company')
    paginator = Paginator(filtered_providers, 16)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    template = 'providers/providers_partial_list.html'
    context = {'providers': page_obj, 'filtered': True, 'requested_type': provider_type}
    data = {'html': render_to_string(template, context, request)}
    return JsonResponse(data)


def create_provider(request):
    """
        DOCSTRING:
        This create_providers function is used to create Providers instances, one of it's functionality
        is to pre-populate the form's provider_type field based on the content the 'HTTP_PROVIDER_TYPE'
        custom header contains, it can be 'LP' for laboratory providers or 'MP' for Medical Providers, if
        the request.method attribute is 'GET' then it will render the template with the form as the only
        content in its context and return the data as a JsonResponse object with a string since we used the
        render_to_string function. If the request.method attribute is 'POST' then it will populate the form
        with the POST request data, check if the form is valid, if not it will render again the form with
        it's errors and send the data as a JsonResponse, if the form is valid it will set the 'created_user'
        field to the user who made the request, afterwards it will extract the provider_type attribute form the
        saved instance, retrieve the updated providers from the database, and render them to the the providers_
        partial_list.html template, as well as the requested_type and the filter_form in it's context, this data
        will be returned as a string in a JsonResponse. It only expects the 'request' parameter as a request object.
    """
    context = {}
    data = {}
    if request.method == 'POST':
        form = ProviderForm(request.POST)
        if form.is_valid():
            try:
                provider = form.save(commit=False)
                provider.created_by = request.user
                provider.save()
                provider_type = 'LP' if provider.provider_type == 'LP' else 'MP'
                updated_providers = Provider.objects.filter(provider_type=provider_type, created_by=request.user).order_by('company')
                is_initial = True if len(updated_providers) == 1 else False
                paginator = Paginator(updated_providers, 16)
                page_obj = paginator.get_page(1)
                template = 'providers/providers_partial_list.html' if is_initial is not True else 'providers/providers_list.html'
                print(template)
                context = {'providers': page_obj, 'filter_form': ProviderFilterForm, 'requested_type': provider_type}
                data = {'updated_html': render_to_string(template, context, request), 'is_initial': is_initial}
                return JsonResponse(data)
            except IntegrityError:
                context['error'] = 'Provider already listed'
    form = ProviderForm(data={'provider_type': 'LP'}) if request.GET.get('provider_type') == 'LP' else ProviderForm(data={'provider_type': 'MP'})
    template = 'providers/create_providers.html'
    context['form'] = form
    data['html'] = render_to_string(template, context, request)
    return JsonResponse(data)


def provider_details(request, pk):
    """
        DOCSTRING:
        The providers_details function is used to retrieve a single provider from the database. The function
        accepts two parameters, the 'request' parameter expects a request object and the 'pk' parameter, a provider's
        instance pk, this parameter is used to retrieve the instance from the database. It renders a template with
        this provider and returns the data as a JsonResponse Object.
    """
    provider = Provider.objects.get(pk=pk)
    template = 'providers/providers_details.html'
    context = {'provider': provider}
    data = {'html': render_to_string(template, context, request)}
    return JsonResponse(data)


def update_provider(request, pk):
    """
        DOCSTRING:
        This update_providers function is used to update Providers instances, it retrieves as single instance from the
         database, using the content of the 'pk' parameter passed to the function, it expects a providers instance pk,
        if the request.method attribute is 'GET' then it will render the template with the form as the only content
        in its context and return the data as a JsonResponse object with a string since we used the render_to_string function.
        If the request.method attribute is 'POST' then it will populate the form with the POST request data, check if the form is valid,
        if not it will render again the form with it's errors and a 'error' which contains a custom error, it will send the data as a JsonResponse,
        if the form is valid it will set the 'created_user' field to the user who made the request, afterwards it will extract the
        provider_type attribute form the saved instance, retrieve the updated providers from the database, and render
        them to the the providers_list.html template, as well as the requested_type and the filter_form in it's
        context, this data will be returned as a string in a JsonResponse. It only expects the 'request' parameter as a request object.
    """
    context = {}
    data = {}
    provider = Provider.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProviderForm(request.POST or None, instance=provider)
        if form.is_valid():
            try:
                provider = form.save(commit=False)
                provider.save()
                provider_type = 'LP' if provider.provider_type == 'LP' else 'MP'
                updated_providers = Provider.objects.filter(provider_type=provider_type, created_by=request.user).order_by('company')
                paginator = Paginator(updated_providers, 16)
                page_obj = paginator.get_page(1)
                template = 'providers/providers_partial_list.html'
                context = {'providers': page_obj, 'filter_form': ProviderFilterForm, 'requested_type': provider_type}
                data = {'updated_html': render_to_string(template, context, request)}
                return JsonResponse(data)
            except IntegrityError:
                context['error'] = 'Provider already listed'
    form = ProviderForm(instance=provider)
    template = 'providers/update_providers.html'
    context['form'] = form
    context['provider'] = provider
    data['html'] = render_to_string(template, context, request)
    return JsonResponse(data)


def delete_provider(request, pk):
    """
        DOCSTRING:
        The providers_delete function is used to retrieve a single provider from the database. The function
        accepts two parameters, the 'request' parameter expects a request object and the 'pk' parameter, a provider's
        instance pk, this parameter is used to retrieve the instance from the database. After the object has been
        retrieved from the database is deleted permanently, and the updated list of providers, rendered to a template
        as well as the filter_form and requested_type extracted from the deleted object before it's deletion. This data
        is returned as a JsonResponse object.
    """
    context = {}
    data = {}
    provider = Provider.objects.get(pk=pk)
    if request.method == 'POST':
        provider_type = provider.provider_type
        provider.delete()
        updated_providers = Provider.objects.filter(provider_type=provider_type, created_by=request.user).order_by('company')
        paginator = Paginator(updated_providers, 16)
        page_obj = paginator.get_page(1)
        template = 'providers/providers_partial_list.html'
        context = {'providers': page_obj, 'filter_form': ProviderFilterForm, 'requested_type':provider_type}
        data['updated_html'] = render_to_string(template, context, request)
        return JsonResponse(data)
    template = 'providers/delete_providers.html'
    context['provider'] = provider
    data['html'] = render_to_string(template, context, request)
    return JsonResponse(data)


# Visitors Related Logic
# ########################################

def visitors_list(request):
    """
        DOCSTRING:
        The visitors_list functions is used to display a list containing all the visitors
        retrieved from the database  we render this content, as well as the filter_form.
        This data is returned by the function as a JsonResponse Object. It only accepts
        one parameter 'request', which expects a request object.
    """
    listed_visitors = Visitor.objects.filter(created_by=request.user).order_by('name')
    paginator = Paginator(listed_visitors, 16)
    page = request.GET.get('page')
    visitors = paginator.get_page(page)
    filter_form = VisitorFilterForm
    template = 'providers/visitors_list.html' if not page else 'providers/visitors_partial_list.html'
    context = {'visitors': visitors, 'filter_form': filter_form}
    data = {'html': render_to_string(template, context, request)}
    return JsonResponse(data)


def filter_visitors(request):
    """
        DOCSTRING:
        The filter_visitors_list function is used to retrieve visitors from the database, it returns only this
        content since the template we render is just a table row, so there is no need to return the filter_form.
        It's only parameter is 'request' and expects an request object.
    """
    query = request.GET.get('query')
    filtered_visitors = Visitor.objects.filter(Q(name__icontains=query) | Q(last_name__icontains=query), created_by=request.user).order_by('name')
    paginator = Paginator(filtered_visitors, 16)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    template = 'providers/visitors_partial_list.html'
    context = {'visitors': page_obj, 'filtered': True}
    data = {'html': render_to_string(template, context, request)}
    return JsonResponse(data)


def create_visitor(request):
    """
        DOCSTRING:
        This create_visitors function is used to create Providers instances, if the request.method attribute
        is 'GET' then it will render the template with the form as the only content in its context and return
        the data as a JsonResponse object with a string since we used the render_to_string function. If the
        request.method attribute is 'POST' then it will populate the form with the POST request data, check
        if the form is valid, if not it will render again the form with it's errors and send the data as a
        JsonResponse, if the form is valid it will set the 'created_user' field to the user who made the request,
        afterwards it will extract the provider_type attribute form the saved instance, retrieve the updated
        providers from the database, and render them to the the visitors_ partial_list.html template, this data
        will be returned as a string in a JsonResponse.  It only expects the 'request' parameter as a request object.
    """
    context = {}
    data = {}
    form = VisitorForm(user=request.user)
    template = 'providers/create_visitor.html'
    if request.method == 'POST':
        form = VisitorForm(request.POST, user=request.user)
        if form.is_valid():
            visitor = form.save(commit=False)
            visitor.created_by = request.user
            visitor.save()
            updated_visitors = Visitor.objects.filter(created_by=request.user).order_by('name')
            is_initial = True if len(updated_visitors) == 1 else False
            template = 'providers/visitors_partial_list.html' if is_initial is not True else 'providers/visitors_list.html'
            paginator = Paginator(updated_visitors, 16)
            page_obj = paginator.get_page(1)
            context = {'visitors': page_obj, 'filter_form': VisitorFilterForm}
            data = {'updated_html': render_to_string(template, context, request), 'is_initial': is_initial}
            return JsonResponse(data)
    context['form'] = form
    data['html'] = render_to_string(template, context, request)
    return JsonResponse(data)


def visitor_details(request, pk):
    """
        DOCSTRING:
        The visitors_details function is used to retrieve a single provider from the database. The function
        accepts two parameters, the 'request' parameter expects a request object and the 'pk' parameter, a visitor's
        instance pk, this parameter is used to retrieve the instance from the database. It renders a template with
        this provider and returns the data as a JsonResponse Object.
    """
    visitor = Visitor.objects.get(pk=pk)
    template = 'providers/visitors_details.html'
    context = {'visitor': visitor}
    data = {'html': render_to_string(template, context, request)}
    return JsonResponse(data)


def update_visitor(request, pk):
    """
        DOCSTRING:
        This update_visitors function is used to update Visitor instances, it retrieves as single instance from the
         database, using the content of the 'pk' parameter passed to the function, it expects a visitor instance pk,
        if the request.method attribute is 'GET' then it will render the template with the form as the only content
        in its context and return the data as a JsonResponse object with a string since we used the render_to_string function.
        If the request.method attribute is 'POST' then it will populate the form with the POST request data, check if the form is valid,
        if not it will render again the form with it's errors and it will send the data as a JsonResponse,  if the form
        is valid it will set the 'created_user' field to the user who made the request, afterwards it will extract the
        provider_type attribute form the saved instance, retrieve the updated visitors from the database, and render
        them to the the visitors_partial_list.html template, the filter_form in it's context, this data will be returned
        as a string in a JsonResponse. It only expects the 'request' parameter as a request object.
    """
    context = {}
    data = {}
    visitor = Visitor.objects.get(pk=pk)
    if request.method == 'POST':
        form = VisitorForm(request.POST or None, user=request.user, instance=visitor)
        if form.is_valid():
            visitor = form.save(commit=False)
            visitor.save()
            template = 'providers/visitors_partial_list.html'
            listed_visitors = Visitor.objects.filter(created_by=request.user).order_by('name')
            paginator = Paginator(listed_visitors, 16)
            page_obj = paginator.get_page(1)
            context = {'visitors': page_obj, 'filter_form': VisitorFilterForm}
            data = {'updated_html': render_to_string(template, context, request)}
            return JsonResponse(data)
    form = VisitorForm(request.POST or None, user=request.user, instance=visitor)
    template = 'providers/update_visitor.html'
    context['form'] = form
    context['visitor'] = visitor
    data['html'] = render_to_string(template, context, request)
    return JsonResponse(data)


def delete_visitor(request, pk):
    """
        DOCSTRING:
        The delete_visitor function is used to retrieve a single visitor from the database. The function
        accepts two parameters, the 'request' parameter expects a request object and the 'pk' parameter, a visitor's
        instance pk, this parameter is used to retrieve the instance from the database. After the object has been
        retrieved from the database is deleted permanently, and the updated list of providers, rendered to a template
        as well as the filter_form. This data is returned as a JsonResponse object.
    """
    context = {}
    data = {}
    visitor = Visitor.objects.get(pk=pk)
    if request.method == 'POST':
        visitor.delete()
        template = 'providers/visitors_partial_list.html'
        listed_visitors = Visitor.objects.filter(created_by=request.user).order_by('name')
        paginator = Paginator(listed_visitors, 16)
        page_obj = paginator.get_page(1)
        context = {'visitors': page_obj, 'filter_form': VisitorFilterForm}
        data = {'updated_html': render_to_string(template, context, request)}
        return JsonResponse(data)
    template = 'providers/delete_visitors.html'
    context['visitor'] = visitor
    data['html'] = render_to_string(template, context, request)
    return JsonResponse(data)









