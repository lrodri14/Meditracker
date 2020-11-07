from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView
from .forms import DoctorSignUpForm, AssistantSignUpForm, ProfileForm
from django.contrib.auth.models import Group
from .models import UsersProfile
from django.views.generic import View
# Create your views here.


class Login(LoginView):
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data()
        data = {'html': render_to_string(self.template_name, context=context, request=self.request)}
        return JsonResponse(data)

    def form_valid(self, form):
        super().form_valid(form)
        data = {'success': 'Login Successful'}
        return JsonResponse(data)

    def form_invalid(self, form):
        context = super().get_context_data()
        data = {'html': render_to_string(self.template_name, context, request=self.request)}
        return JsonResponse(data)


class Logout(LogoutView):
    pass


class ChangePassword(PasswordChangeView):
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('accounts:change_password_done')

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        data = {'html': render_to_string(self.template_name, context=context, request=self.request)}
        return JsonResponse(data)

    def form_valid(self, form):
        super().form_valid(form)
        data = {'success': True}
        return JsonResponse(data)

    def form_invalid(self, form):
        context = super().get_context_data()
        data = {'html': render_to_string(self.template_name, context, self.request)}
        return JsonResponse(data)


class ChangePasswordDone(PasswordChangeDoneView):
    template_name = 'accounts/change_password_done.html'


class PasswordReset(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset.txt'
    success_url = reverse_lazy('accounts:password_reset_done')

    def get(self, request, *args, **kwargs):
        context = super().get_context_data()
        data = {'html': render_to_string(self.template_name, context, self.request)}
        return JsonResponse(data)


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data()
        data = {'html': render_to_string(self.template_name, context, self.request)}
        return JsonResponse(data)


class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'


def signup(request):
    context = {}
    data = {}
    account_type = request.META.get('HTTP_TYPE')
    form = DoctorSignUpForm if account_type == 'doctor' else AssistantSignUpForm
    context['form'] = form
    if request.method == 'POST':
        doctor = Group.objects.get(name='Doctor')
        assistant = Group.objects.get(name='Assistant')
        form = DoctorSignUpForm(request.POST) if 'speciality' in request.POST else AssistantSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data.get('speciality'):
                user.roll = 'Doctor'
                user.save()
                user.groups.add(doctor)
            else:
                user.roll = 'Assistant'
                user.save()
                user.groups.add(assistant)
        else:
            context['form'] = form
            data['error'] = 'Invalid Information'
    data['html'] = render_to_string('accounts/signup.html', context, request)
    return JsonResponse(data)


def profile(request):
    user_profile = get_object_or_404(UsersProfile, user=request.user)
    context = {'user_profile': user_profile}
    return render(request, 'accounts/profile.html', context)


def profile_change(request):
    user_profile = get_object_or_404(UsersProfile, user=request.user)
    form = ProfileForm(instance=user_profile)
    template = 'accounts/profile_change.html'
    context = {}
    data = {}
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            context['user_profile'] = user_profile
            data['success'] = render_to_string('accounts/partial_profile.html', context=context, request=request)
    context['form'] = form
    data['html'] = render_to_string(template, context, request)
    return JsonResponse(data)
