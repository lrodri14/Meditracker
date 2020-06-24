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
    profile = get_object_or_404(UsersProfile, user=request.user)
    form = ProfileForm(request.POST or None, instance=profile)
    if form.is_valid():
        form.save()
    return render(request, 'accounts/profile_change.html', {'form': form})
