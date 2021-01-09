from django.urls import path
from .views import Login, Logout, ChangePassword, ChangePasswordDone, PasswordReset, PasswordResetDone, \
    PasswordResetConfirm, PasswordResetComplete, signup, profile_change,profile_picture_change, \
    profile_background_change, profile, user_lookup

app_name = 'accounts'
urlpatterns = [
    path('login', Login.as_view(), name='login'),
    path('logout', Logout.as_view(), name='logout'),
    path('change_password', ChangePassword.as_view(), name='change_password'),
    path('change_password_done', ChangePasswordDone.as_view(), name='change_password_done'),
    path('password_reset', PasswordReset.as_view(), name='password_reset'),
    path('password_reset_done', PasswordResetDone.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('password_reset_complete', PasswordResetComplete.as_view(), name='password_reset_complete'),
    path('signup', signup, name='signup'),
    path('profile', profile, name='profile'),
    path('profile/<int:pk>', profile, name='profile'),
    path('profile_picture_change', profile_picture_change, name='profile_picture_change'),
    path('profile_background_change', profile_background_change, name='profile_background_change'),
    path('profile_change', profile_change, name='profile_change'),
    path('user_lookup', user_lookup, name='user_lookup')
]