from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from patients.models import Patient
from appointments.models import Consults
from appointments.forms import RecordsDateFilterForm


def records_list(request):
    appointments_list = Consults.objects.filter(created_by=request.user, medical_status=True,).order_by('-datetime')
    paginator = Paginator(appointments_list, 25)
    page = request.GET.get('page')
    appointments = paginator.get_page(page)
    form = RecordsDateFilterForm
    template = 'records/records_list.html'
    context = {'appointments': appointments, 'form': form}
    if request.method == 'POST':
        form = RecordsDateFilterForm(request.POST)
        if form.is_valid():
            from_date = form.cleaned_data['date_from']
            to_date = form.cleaned_data['date_to']
            appointments = Consults.objects.filter(datetime__date__gte=from_date, datetime__date__lte=to_date, medical_status=True, created_by=request.user)
            if len(appointments) > 0:
                context['appointments'] = appointments
            else:
                context['error'] = 'No records found'
            data = {'html': render_to_string('records/partial_records_list.html', context, request)}
            return JsonResponse(data)
    return render(request, template, context)


def filtered_records(request, pk):
    patient = Patient.objects.get(pk=pk)
    records = Consults.objects.filter(created_by=request.user, medical_status=True, patient=patient).order_by('-datetime')
    template = 'records/filtered_records.html'
    context = {'records': records}
    data = {'html': render_to_string(template, context, request)}
    return JsonResponse(data)
