from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView
from .forms import SignUpForm, ProfileForm
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
    if request.method == 'POST':
        doctor = Group.objects.get(name='Doctor')
        assistant = Group.objects.get(name='Assistant')
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            if user.roll == 'Assistant':
                user.groups.add(assistant)
            else:
                user.groups.add(doctor)
            user.save()
            return redirect('accounts:login')
    else:
        form = SignUpForm()
        context['form'] = form
        data['html'] = render_to_string('accounts/signup.html', context, request)
    return JsonResponse(data)


def profile(request):
    return render(request, 'accounts/profile.html')


def profile_change(request):
    user_profile = get_object_or_404(UsersProfile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['profile_pic']:
                user_profile.profile_pic = form.cleaned_data['profile_pic']
            elif 'profile_pic-clear' in request.POST and request.POST['profile_pic-clear']:
                user_profile.profile_pic = None
            else:
                user_profile.profile_pic = user_profile.profile_pic
                user_profile.bio = form.cleaned_data['bio']
                user_profile.phone_number = form.cleaned_data['phone_number']
                user_profile.birth_date = form.cleaned_data['birth_date']
                user_profile.origin = form.cleaned_data['origin']
                user_profile.gender = form.cleaned_data['gender']
                user_profile.location = form.cleaned_data['location']
                user_profile.address = form.cleaned_data['address']
                user_profile.tzone = form.cleaned_data['tzone']
                user_profile.save()
                return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=user_profile)
    return render(request, 'accounts/profile_change.html', context={'form': form, 'user': request.user})

