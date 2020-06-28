from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import Login, Logout, ChangePassword, ChangePasswordDone, PasswordReset, PasswordResetDone, \
    PasswordResetConfirm, PasswordResetComplete, signup, profile_change, profile

app_name = 'accounts'
urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('change_password/', ChangePassword.as_view(), name='change_password'),
    path('change_password_done/', ChangePasswordDone.as_view(), name='change_password_done'),
    path('password_reset/', PasswordReset.as_view(), name='password_reset'),
    path('password_reset_done/', PasswordResetDone.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', PasswordResetComplete.as_view(), name='password_reset_complete'),
    path('signup/', signup, name='signup'),
    path('profile/', profile, name='profile'),
    path('profile_change/', profile_change, name='profile_change'),
]