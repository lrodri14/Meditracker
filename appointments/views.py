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
from .tasks import change_status, save_new_drug
from django.core.paginator import Paginator
from weasyprint import HTML
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
# Create your views here.


def consults(request):
    change_status.delay()
    today = timezone.localtime(timezone.now())
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
    try:
        if request.method == 'POST':
            consults_form = ConsultsForm(request.user, request.POST)
            if consults_form.is_valid():
                consult = consults_form.save(commit=False)
                consult.created_by = request.user
                consult.save()
                return redirect(reverse('appointments:consults'))
    except IntegrityError:
            context['unique_error'] = 'There is a consult created for that date and time already'
            return render(request, template, context)
    return render(request, template, context)


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


def cancel_consult(request, pk):
    try:
        consult = Consults.objects.get(pk=pk)
        if consult.status == 'OPEN':
            template = 'appointments/delete_consult.html'
        else:
            template = 'appointments/delete_consult.html'
        context = {'consult': consult}
        if request.method == 'POST':
            if request.POST['choice'] == 'yes':
                consult.status = 'CANCELLED'
                consult.save()
                return redirect(reverse('appointments:consults'))
            else:
                return redirect(reverse('appointments:consult_register'))
        return render(request, template, context)
    except ObjectDoesNotExist:
        return redirect(reverse('appointments:consult_register'))


def agenda(request):
    today = timezone.localtime(timezone.now())
    form = AgendaDateFilterForm
    consults = Consults.objects.filter(created_by=request.user, datetime__date__month__gte=today.month, medical_status=False).order_by('datetime')
    months = []
    for x in consults:
        if x.datetime.month not in months:
            months.append(x.datetime.month)
    months_names = []
    for x in months:
        months_names.append(calendar.month_name[x])
    template = 'appointments/consults_register.html'
    context = {'consults': consults, 'form': form, 'months': months_names}
    if request.method == 'POST':
        form = AgendaDateFilterForm(request.POST)
        if form.is_valid():
            from_date = form.cleaned_data['date_from']
            to_date = form.cleaned_data['date_to']
            consults = Consults.objects.filter(datetime__date__gte=from_date, datetime__date__lte=to_date, medical_status=False, created_by=request.user).order_by('datetime')
            months = []
            for x in consults:
                if x.datetime.month not in months:
                    months.append(x.datetime.month)
            months_names = []
            for x in months:
                months_names.append(calendar.month_name[x])
            context['consults'] = consults
            context['months'] = months_names
            return render(request, template, context)
    return render(request, template, context)


def registers(request):
    consults_list = Consults.objects.filter(created_by=request.user).order_by('-datetime')
    paginator = Paginator(consults_list, 25)
    page = request.GET.get('page')
    consults = paginator.get_page(page)
    template = 'appointments/registers.html'
    form = RegistersFilter
    context = {'consults': consults, 'form':form, 'items': len(consults_list)}
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
                consults = Consults.objects.filter(Q(patient__first_names__icontains=patient)|Q(patient__last_names__icontains=patient), created_by=request.user)
                context['consults'] = consults
                context['items'] = len(consults)
            elif month and patient == '' and int(year) == 1920:
                consults = Consults.objects.filter(datetime__date__month=month, created_by=request.user)
                context['consults'] = consults
                context['items'] = len(consults)
            elif int(year) != 1920 and patient == '' and int(month) == 0:
                consults = Consults.objects.filter(datetime__date__year=year, created_by=request.user)
                context['consults'] = consults
                context['items'] = len(consults)
            elif patient and int(month) != 0 and int(year)==1920:
                consults = Consults.objects.filter(Q(patient__first_names__icontains=patient)|Q(patient__last_names__icontains=patient),datetime__date__month=month, created_by=request.user)
                context['consults'] = consults
                context['items'] = len(consults)
            elif patient and int(year) != 1920 and int(month) == 0:
                consults = Consults.objects.filter(Q(patient__first_names__icontains=patient)|Q(patient__last_names__icontains=patient),datetime__date__year=year, created_by=request.user)
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
    context = {'user':user, 'consult':consult}
    template = render_to_string('appointments/pdf.html', context)
    pdf = HTML(string=template, base_url=request.build_absolute_uri()).write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="result.pdf"'
    return response
