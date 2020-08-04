from django.conf import settings
from django.shortcuts import redirect
from django.utils import timezone
import pytz


class LoginRequiredMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        view_names = ['Login', 'signup', 'main', 'PasswordReset',
                      'PasswordResetDone', 'PasswordResetConfirm', 'PasswordResetComplete']
        if request.user.is_authenticated and view_func.__name__ in view_names:
            return redirect(settings.LOGIN_REDIRECT_URL)
        elif request.user.is_authenticated or view_func.__name__ in view_names:
            return None
        else:
            return redirect(settings.LOGIN_URL)


class TimezoneMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            tzname = request.user.profile.tzone
            if tzname:
                timezone.activate(pytz.timezone(tzname))
            else:
                timezone.deactivate()
        else:
            pass
        return self.get_response(request)





