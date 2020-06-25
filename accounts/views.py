from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView
from .forms import SignUpForm, ProfileForm
from .models import UsersProfile
# Create your views here.


class Login(LoginView):
    template_name = 'accounts/login.html'


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


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def profile_change(request):
    user_profile = get_object_or_404(UsersProfile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile.profile_pic = form.cleaned_data['profile_pic']
            user_profile.bio = form.cleaned_data['bio']
            user_profile.phone_number = form.cleaned_data['phone_number']
            user_profile.birth_date = form.cleaned_data['birth_date']
            user_profile.gender = form.cleaned_data['gender']
            user_profile.location = form.cleaned_data['location']
            user_profile.address = form.cleaned_data['address']
            user_profile.save()
    else:
        form = ProfileForm(instance=user_profile)
    return render(request, 'accounts/profile_change.html',context={'form': form, 'user': user_profile})

