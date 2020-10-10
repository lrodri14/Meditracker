from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from patients.models import Patient
from appointments.models import Consults
from appointments.forms import RecordsDateFilterForm


def records_list(request, pk=None):
    appointments_list = Consults.objects.filter(created_by=request.user, medical_status=True,).order_by('-datetime') if pk == None else Consults.objects.filter(created_by=request.user, medical_status=True, patient=Patient.objects.get(pk=pk)).order_by('-datetime')
    paginator = Paginator(appointments_list, 25)
    page = request.GET.get('page')
    appointments = paginator.get_page(page)
    form = RecordsDateFilterForm
    template = 'records/records_list.html'
    context = {'appointments': appointments, 'form': form}
    context['referer'] = request.META['HTTP_REFERER'] if 'update_consult' in request.META['HTTP_REFERER'] else None
    if request.method == 'POST' and not pk:
        form = RecordsDateFilterForm(request.POST)
        if form.is_valid():
            from_date = form.cleaned_data['date_from']
            to_date = form.cleaned_data['date_to']
            appointments = Consults.objects.filter(datetime__date__gte=from_date, datetime__date__lte=to_date, medical_status=True, created_by=request.user)
            if len(appointments) > 0:
                context['appointments'] = appointments
            else:
                context['error'] = 'There are no consults for these dates'
            data = {'html': render_to_string('records/partial_records_list.html', context, request)}
            return JsonResponse(data)
    return render(request, template, context)