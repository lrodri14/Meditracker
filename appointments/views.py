from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from .models import Consults
from patients.models import Patient
from .forms import ConsultsForm, UpdateConsultsForm, RecordsDateFilterForm, AgendaDateFilterForm, RegistersFilter
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group
from django.db import IntegrityError
from django.db.models import Q
import calendar
from .tasks import save_new_drug
from django.core.paginator import Paginator
from weasyprint import HTML
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth import get_user_model

# Create your views here.


def consults(request):
    today = timezone.localtime()
    doctor_group = Group.objects.get(name='Doctor')
    doctor = doctor_group in request.user.groups.all()
    appointments = Consults.objects.filter(created_by=request.user, datetime__date=today.date(), medical_status=False, status='CONFIRMED')
    template = 'appointments/consults.html'
    context = {'appointments': appointments, 'today': today, 'doctor': doctor}
    return render(request, template, context)


def consults_list(request, pk=None):
    appointments_list = Consults.objects.filter(created_by=request.user, medical_status=True).order_by('-datetime')
    paginator = Paginator(appointments_list, 25)
    page = request.GET.get('page')
    appointments = paginator.get_page(page)
    form = RecordsDateFilterForm
    template = 'appointments/consults_list.html'
    context = {'appointments': appointments, 'form': form}
    if pk:
        patient = Patient.objects.get(pk=pk)
        appointments = Consults.objects.filter(created_by=request.user, medical_status=True, patient=patient)
        form = RecordsDateFilterForm
        template = 'appointments/consults_list.html'
        context = {'appointments': appointments, 'form': form}
        return render(request, template, context)
    if request.method == 'POST':
        form = RecordsDateFilterForm(request.POST)
        if form.is_valid():
            from_date = form.cleaned_data['date_from']
            to_date = form.cleaned_data['date_to']
            context['appointments'] = Consults.objects.filter(datetime__date__gte=from_date, datetime__date__lte=to_date, medical_status=True, created_by=request.user)
            return render(request, template, context)
    return render(request, template, context)


def create_consult(request):
    consults_form = ConsultsForm(user=request.user)
    template = 'appointments/create_consult.html'
    context = {'consults_form': consults_form}
    data = {'html': render_to_string(template, context, request)}
    if request.method == 'POST':
        consults_form = ConsultsForm(request.user, request.POST)
        if consults_form.is_valid():
            consult = consults_form.save(commit=False)
            consult.created_by = request.user
            consult.save()
            data = {'success': 'Patient created successfully'}
        else:
            context['unique_error'] = 'There is a consult created for that date and time already.'
            data = {'html': render_to_string(template, context, request)}
    return JsonResponse(data)


def consults_details(request, pk):
    consult = Consults.objects.get(pk=pk)
    template = 'appointments/consult_details.html'
    context = {'consult': consult}
    return render(request, template, context)


def update_consult(request, pk):
    consult = Consults.objects.get(pk=pk)
    consult_form = UpdateConsultsForm(request.user, request.POST or None, instance=consult)
    template = 'appointments/update_consult.html'
    context = {'consult': consult, 'consult_form': consult_form}
    if request.method == 'POST':
        consult_form = UpdateConsultsForm(request.user, request.POST or None, instance=consult)
        if consult_form.is_valid():
            consult = consult_form.save(commit=False)
            if consult.medicine != '':
                save_new_drug.delay(drugs=list(consult.medicine.splitlines()), user_id=request.user.id)
            consult.medical_status = True
            consult.save()
            consult_form.save_m2m()
            return redirect('appointments:consults')
    return render(request, template, context)

# Cancel Consult


def cancel_consult(request, pk):
    today = timezone.localtime(timezone.now())
    consult = Consults.objects.get(pk=pk)
    consults = Consults.objects.filter(created_by=request.user, datetime__date__month__gte=today.month, medical_status=False).order_by('datetime')
    template = 'appointments/delete_consult.html'
    context = {'consult': consult}
    data = {'html': render_to_string(template, context, request)}
    if request.method == 'POST':
        consult.status = 'CANCELLED'
        consult.save()
        tzone = timezone.get_current_timezone()
        form = AgendaDateFilterForm
        updated_consults = Consults.objects.filter(created_by=request.user, datetime__date__gte=today.date(), medical_status=False).order_by('datetime')
        months = []
        for c in consults:
            if c.datetime.astimezone(tzone).month not in months:
                months.append(c.datetime.month)
        months_names = []
        for x in months:
            months_names.append(calendar.month_name[x])
        data = {'html': render_to_string('appointments/partial_consults_register_list.html', {'consults': updated_consults, 'months': months_names, 'form':form}, request=request)}
    return JsonResponse(data)


def agenda(request):
    today = timezone.localtime()
    tzone = timezone.get_current_timezone()
    form = AgendaDateFilterForm
    consults = Consults.objects.filter(created_by=request.user, datetime__date__gte=today.date(), medical_status=False).order_by('datetime')
    months = []
    for c in consults:
        if c.datetime.astimezone(tzone).month not in months:
            months.append(c.datetime.month)
    months_names = []
    for x in months:
        months_names.append(calendar.month_name[x])
    template = 'appointments/consults_register.html'
    context = {'consults': consults, 'form': form, 'months': months_names, 'today': today}
    if request.method == 'POST':
        form = AgendaDateFilterForm(request.POST)
        if form.is_valid():
            from_date = form.cleaned_data['date_from']
            to_date = form.cleaned_data['date_to']
            consults = Consults.objects.filter(datetime__date__gte=from_date, datetime__date__lte=to_date, medical_status=False, created_by=request.user).order_by('datetime')
            months = []
            for c in consults:
                if c.datetime.astimezone(tzone).month not in months:
                    months.append(c.datetime.month)
            months_names = []
            for x in months:
                months_names.append(calendar.month_name[x])
            context['consults'] = consults
            context['months'] = months_names
            return render(request, template, context)
    return render(request, template, context)


def registers(request):
    today = timezone.localtime()
    tzone = timezone.get_current_timezone()
    consults_list = Consults.objects.filter(created_by=request.user).order_by('-datetime')
    not_attended_consults = Consults.objects.filter(created_by=request.user, datetime__date__lte=today.date(), medical_status=False)
    print(not_attended_consults)
    paginator = Paginator(consults_list, 25)
    page = request.GET.get('page')
    consults = paginator.get_page(page)
    template = 'appointments/registers.html'
    form = RegistersFilter
    context = {'consults': consults, 'form':form, 'items': len(consults_list), 'today': today}
    for na in not_attended_consults:
        if na.datetime.astimezone(tzone).date() < today.date():
            na.status = 'CLOSED'
            na.save()
    if request.method == 'POST':
        form = RegistersFilter(request.POST)
        if form.is_valid():
            patient = form.cleaned_data['patient']
            month = form.cleaned_data['month']
            year = form.cleaned_data['year']
            if patient == '' and int(month) == 0 and int(year) == 1920:
                context['consults'] = Consults.objects.filter(created_by=request.user).order_by('-datetime')
                context['error'] = 'You need to provide at least one value in the fields.'
            elif patient and int(month) == 0 and int(year) == 1920:
                consults = Consults.objects.filter(Q(patient__first_names__icontains=patient)|Q(patient__last_names__icontains=patient),
                                                   created_by=request.user)
                context['consults'] = consults
                context['items'] = len(consults)
            elif month and patient == '' and int(year) == 1920:
                consults = Consults.objects.filter(datetime__date__month=month,
                                                   created_by=request.user)
                context['consults'] = consults
                context['items'] = len(consults)
            elif int(year) != 1920 and patient == '' and int(month) == 0:
                consults = Consults.objects.filter(datetime__date__year=year,
                                                   created_by=request.user)
                context['consults'] = consults
                context['items'] = len(consults)
            elif patient and int(month) != 0 and int(year)==1920:
                consults = Consults.objects.filter(Q(patient__first_names__icontains=patient)|Q(patient__last_names__icontains=patient),
                                                   datetime__date__month=month,
                                                   created_by=request.user)
                context['consults'] = consults
                context['items'] = len(consults)
            elif patient and int(year) != 1920 and int(month) == 0:
                consults = Consults.objects.filter(Q(patient__first_names__icontains=patient)|Q(patient__last_names__icontains=patient),
                                                   datetime__date__year=year,
                                                   created_by=request.user)
                context['consults'] = consults
                context['items'] = len(consults)
    return render(request, template, context)


def consult_date_update(request, pk):
    consult = Consults.objects.get(pk=pk)
    consult_form = ConsultsForm(request.user, request.POST or None, instance=consult)
    template = 'appointments/consult_date_update.html'
    context = {'consult_form': consult_form}
    if request.method == 'POST':
        if consult_form.is_valid():
            consult_form.save()
            return redirect('appointments:agenda')
        else:
            context['error'] = 'Please insert all the valid values.'
            return render(request, template, context)
    return render(request, template, context)


def consult_confirm(request, pk):
    consult = Consults.objects.get(pk=pk)
    consult.status = 'CONFIRMED'
    consult.save()
    return redirect(reverse('appointments:agenda'))


def generate_pdf(request, pk):
    user = get_user_model().objects.get(pk=request.user.pk)
    consult = Consults.objects.get(pk=pk)
    context = {'user': user, 'consult': consult}
    template = render_to_string('appointments/pdf.html', context)
    pdf = HTML(string=template, base_url=request.build_absolute_uri()).write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="result.pdf"'
    return response
