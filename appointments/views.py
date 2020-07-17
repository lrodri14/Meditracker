from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from .models import Consults
from .forms import ConsultsForm, UpdateConsultsForm
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group
# Create your views here.


# Doctor Views
def consults(request):
    today = timezone.now()
    doctor_group = Group.objects.get(name='Doctor')
    doctor = doctor_group in request.user.groups.all()
    appointments = Consults.objects.filter(created_by=request.user, datetime__date=today.date(), status=0)
    template = 'appointments/consults.html'
    context = {'appointments': appointments, 'today': today, 'doctor': doctor}
    return render(request, template, context)


def consults_list(request):
    appointments = Consults.objects.filter(created_by=request.user)
    template = 'appointments/consults_list.html'
    context = {'appointments': appointments}
    return render(request, template, context)


def create_consult(request):
    consults_form = ConsultsForm
    template = 'appointments/create_consult.html'
    context = {'consults_form': consults_form}
    if request.method == 'POST':
        consults_form = ConsultsForm(request.POST)
        if consults_form.is_valid():
            consult = consults_form.save(commit=False)
            consult.created_by = request.user
            consult.save()
            return redirect(reverse('appointments:consults'))
        else:
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
    consult_form = UpdateConsultsForm(instance=consult)
    template = 'appointments/update_consult.html'
    context = {'consult': consult, 'consult_form': consult_form}
    if request.method == 'POST':
        if consult_form.is_valid():
            consult_form.save()
            return redirect('appointments:consults')
    return render(request, template, context)


def delete_consult(request, pk):
    try:
        consult = Consults.objects.get(pk=pk)
        if consult.status < 1:
            template = 'appointments/delete_consult.html'
        else:
            template = 'appointments/consult_delete_exception.html'
        context = {'consult': consult}
        if request.method == 'POST':
            if request.POST['choice'] == 'yes':
                consult.delete()
                return redirect(reverse('appointments:consults'))
            else:
                return redirect(reverse('appointments:consults_list'))
        return render(request, template, context)
    except ObjectDoesNotExist:
        return redirect(reverse('appointments:consults_list'))


# Assistant Views
def consults_register(request):
    today = timezone.now().date()
    consults = Consults.objects.filter(created_by=request.user, datetime__date__gte=today)
    template = 'appointments/consults_register.html'
    context = {'consults': consults}
    return render(request, template, context)


def consult_date_update(request, pk):
    consult = Consults.objects.get(pk=pk)
    consult_form = ConsultsForm(instance=consult)
    template = 'appointments/consult_date_update.html'
    context = {'consult_form': consult_form}
    if request.method == 'POST':
        if consult_form.is_valid():
            consult_form.save()
        else:
            context['error'] = 'Please insert all the valid values.'
            return render(request, template, context)
    return render(request, template, context)


def consult_cancel(request, pk):
    try:
        consult = Consults.objects.get(pk=pk)
        template = 'appointments/consult_cancel.html'
        context = {'consult': consult}
        if request.method == 'POST':
            if request.POST['choice'] == 'Yes':
                consult.delete()
                return redirect(reverse('appointments:consult_register'))
            else:
                return redirect(reverse('appointments:consult_register'))
        return render(request, template, context)
    except ObjectDoesNotExist:
        return reverse(redirect('appointments:consult_register'))
