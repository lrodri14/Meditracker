from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView
from .forms import DoctorSignUpForm, AssistantSignUpForm, ProfileForm, ProfilePictureForm, ProfileBackgroundForm
from django.contrib.auth.models import Group
from .models import UsersProfile
from utilities.accounts_utilities import set_mailing_credentials
from django.contrib.auth import get_user_model
User = get_user_model()

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
        super().form_invalid(form)
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
    data = {}
    account_type = request.GET.get('account_type')
    form = DoctorSignUpForm if account_type == 'doctor' else AssistantSignUpForm
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
                set_mailing_credentials(user.email, user)
            else:
                user.roll = 'Assistant'
                user.save()
                user.groups.add(assistant)
        else:
            data['error'] = True
    context = {'form': form}
    data['html'] = render_to_string('accounts/signup.html', context, request)
    return JsonResponse(data)


def profile(request, pk=None):
    user = User.objects.get(username=request.user) if not pk else User.objects.get(pk=pk)
    context = {'user': user, 'authenticated_user': request.user}
    return render(request, 'accounts/profile.html', context)


def profile_picture_change(request):
    form = ProfilePictureForm(instance=request.user.profile)
    template = 'accounts/profile_picture_change.html'
    context = {}
    data = {}
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            context['user'] = request.user
            context['authenticated_user'] = request.user
            data['success'] = render_to_string('accounts/partial_profile.html', context=context, request=request)
    context['form'] = form
    data['html'] = render_to_string(template, context, request)
    return JsonResponse(data)


def profile_background_change(request):
    form = ProfileBackgroundForm(instance=request.user.profile)
    template = 'accounts/profile_background_change.html'
    context = {}
    data = {}
    if request.method == 'POST':
        form = ProfileBackgroundForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            context['user'] = request.user
            context['authenticated_user'] = request.user
            data['success'] = render_to_string('accounts/partial_profile.html', context=context, request=request)
    context['form'] = form
    data['html'] = render_to_string(template, context, request)
    return JsonResponse(data)


def profile_change(request):
    form = ProfileForm(instance=request.user.profile)
    template = 'accounts/profile_change.html'
    context = {}
    data = {}
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            context['user'] = request.user
            context['authenticated_user'] = request.user
            data['success'] = render_to_string('accounts/partial_profile.html', context=context, request=request)
    context['form'] = form
    context['user_profile'] = request.user.profile
    data['html'] = render_to_string(template, context, request)
    return JsonResponse(data)


def user_lookup(request):
    query = request.GET.get('query')
    close_users = User.objects.filter(Q(username__startswith=query) | Q(first_name__startswith=query) | Q(last_name__startswith=query)).order_by('first_name')
    # other_users = User.objects.filter(Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query)).order_by('first_name')
    users = close_users
    template = 'accounts/users_lookup_results.html'
    context = {'users': users}
    data = {'html': render_to_string(template, context, request)}
    return JsonResponse(data)
