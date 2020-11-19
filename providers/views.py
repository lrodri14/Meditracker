from django.db import IntegrityError
from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
from .models import Providers, Visitor
from .forms import ProvidersForm, ProvidersFilterForm, VisitorsForm, VisitorsFilterForm

# Create your views here.

# Providers
# Main Providers View


def providers(request):
    providers = True if len(Providers.objects.filter(created_by=request.user)) > 0 else False
    template = 'providers/providers.html'
    context = {'providers': providers}
    return render(request, template, context)


# Providers List View


def providers_list(request):
    requested_type = request.META.get('HTTP_PROVIDER_TYPE')
    provider_type = 'LP' if requested_type == 'LP' else 'MP'
    providers_created = Providers.objects.filter(provider_type=provider_type, created_by=request.user)
    filter_form = ProvidersFilterForm
    template = 'providers/providers_partial_list.html'
    context = {'providers': providers_created, 'filter_form': filter_form,'requested_type': requested_type}
    data = {'html': render_to_string(template, context, request)}
    return JsonResponse(data)


# Providers Filter View


def filter_providers_list(request):
    query = request.META.get('HTTP_QUERY')
    provider_type = request.META.get('HTTP_PROVIDER_TYPE')
    filter_providers = Providers.objects.filter(company__icontains=query, provider_type=provider_type, created_by=request.user)
    template = 'providers/providers_filtered_list.html'
    context = {'providers': filter_providers}
    data = {'html': render_to_string(template, context, request)}
    return JsonResponse(data)


# Providers Creation View


def create_providers(request):
    context = {}
    data = {}
    if request.method == 'POST':
        form = ProvidersForm(request.POST)
        if form.is_valid():
            try:
                provider = form.save(commit=False)
                provider.created_by = request.user
                provider.save()
                provider_type = 'LP' if provider.provider_type == 'LP' else 'MP'
                updated_provider = Providers.objects.filter(provider_type=provider_type, created_by=request.user)
                template = 'providers/providers_partial_list.html'
                context = {'providers': updated_provider, 'filter_form': ProvidersFilterForm, 'requested_type':provider_type}
                data = {'updated_html': render_to_string(template, context, request)}
                return JsonResponse(data)
            except IntegrityError:
                context['error'] = 'Provider already listed'
    form = ProvidersForm(data={'provider_type': 'LP'}) if request.META.get('HTTP_FORM_TYPE') == 'LP' else ProvidersForm(data={'provider_type': 'MP'})
    template = 'providers/create_providers.html'
    context['form'] = form
    data['html'] = render_to_string(template, context, request)
    return JsonResponse(data)


# Providers Details View


def providers_details(request, pk):
    provider = Providers.objects.get(pk=pk)
    template = 'providers/providers_details.html'
    context = {'provider': provider}
    data = {'html': render_to_string(template, context, request)}
    return JsonResponse(data)


# Providers Updating View


def update_providers(request, pk):
    context = {}
    data = {}
    provider = Providers.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProvidersForm(request.POST or None, instance=provider)
        if form.is_valid():
            try:
                provider = form.save(commit=False)
                provider.save()
                provider_type = 'LP' if provider.provider_type == 'LP' else 'MP'
                updated_provider = Providers.objects.filter(provider_type=provider_type, created_by=request.user)
                template = 'providers/providers_partial_list.html'
                context = {'providers': updated_provider, 'filter_form': ProvidersFilterForm, 'requested_type':provider_type}
                data = {'updated_html': render_to_string(template, context, request)}
                return JsonResponse(data)
            except IntegrityError:
                context['error'] = 'Provider already listed'
    form = ProvidersForm(instance=provider)
    template = 'providers/update_providers.html'
    context['form'] = form
    context['provider'] = provider
    data['html'] = render_to_string(template, context, request)
    return JsonResponse(data)


# Providers Deletion View


def delete_provider(request, pk):
    context = {}
    data = {}
    provider = Providers.objects.get(pk=pk)
    if request.method == 'POST':
        provider_type = provider.provider_type
        provider.delete()
        updated_providers = Providers.objects.filter(provider_type=provider_type, created_by=request.user)
        template = 'providers/providers_partial_list.html'
        context = {'providers': updated_providers, 'filter_form': ProvidersFilterForm, 'requested_type':provider_type}
        data['updated_html'] = render_to_string(template, context, request)
        return JsonResponse(data)
    template = 'providers/delete_providers.html'
    context['provider'] = provider
    data['html'] = render_to_string(template, context, request)
    return JsonResponse(data)


# Visitors
# Visitors List

def visitors_list(request):
    visitors = Visitor.objects.filter(created_by=request.user)
    filter_form = VisitorsFilterForm
    template = 'providers/visitors_partial_list.html'
    context = {'visitors': visitors, 'filter_form': filter_form}
    data = {'html': render_to_string(template, context, request)}
    return JsonResponse(data)


# Filter Visitors
def filter_visitors_list(request):
    query = request.META.get('HTTP_QUERY')
    filtered_visitors = Visitor.objects.filter(Q(name__icontains=query) | Q(last_name__icontains=query), created_by=request.user)
    template = 'providers/visitors_filtered_list.html'
    context = {'visitors': filtered_visitors, 'filter_form': VisitorsFilterForm}
    data = {'html': render_to_string(template, context, request)}
    return JsonResponse(data)

# Visitors Create


def create_visitor(request):
    context = {}
    data = {}
    form = VisitorsForm(user=request.user)
    template = 'providers/create_visitor.html'
    if request.method == 'POST':
        form = VisitorsForm(request.POST, user=request.user)
        if form.is_valid():
            visitor = form.save(commit=False)
            visitor.created_by = request.user
            visitor.save()
            template = 'providers/visitors_partial_list.html'
            updated_visitors = Visitor.objects.filter(created_by=request.user)
            context['visitors'] = updated_visitors
            context['filter_form'] = VisitorsFilterForm
            data['updated_html'] = render_to_string(template, context, request)
            return JsonResponse(data)
    context['form'] = form
    data['html'] = render_to_string(template, context, request)
    return JsonResponse(data)


# Visitors details


def visitors_details(request, pk):
    visitor = Visitor.objects.get(pk=pk)
    template = 'providers/visitors_details.html'
    context = {'visitor': visitor}
    data = {'html': render_to_string(template, context, request)}
    return JsonResponse(data)


# Visitors update


def update_visitors(request, pk):
    context = {}
    data = {}
    visitor = Visitor.objects.get(pk=pk)
    if request.method == 'POST':
        form = VisitorsForm(request.POST or None, user=request.user, instance=visitor)
        if form.is_valid():
            visitor = form.save(commit=False)
            visitor.save()
            updated_visitor = Visitor.objects.filter(created_by=request.user)
            template = 'providers/visitors_partial_list.html'
            context = {'visitors': updated_visitor, 'filter_form': VisitorsFilterForm}
            data = {'updated_html': render_to_string(template, context, request)}
            return JsonResponse(data)
    form = VisitorsForm(request.POST or None, user=request.user, instance=visitor)
    template = 'providers/update_visitor.html'
    context['form'] = form
    context['visitor'] = visitor
    data['html'] = render_to_string(template, context, request)
    return JsonResponse(data)


# Visitor's Delete

def delete_visitor(request, pk):
    context = {}
    data = {}
    visitor = Visitor.objects.get(pk=pk)
    if request.method == 'POST':
        visitor.delete()
        updated_visitors = Visitor.objects.filter(created_by=request.user)
        template = 'providers/visitors_partial_list.html'
        context['visitors'] = updated_visitors
        context['filter_form'] = VisitorsFilterForm
        data['updated_html'] = render_to_string(template, context, request)
        return JsonResponse(data)
    template = 'providers/delete_visitors.html'
    context['visitor'] = visitor
    data['html'] = render_to_string(template, context, request)
    return JsonResponse(data)









