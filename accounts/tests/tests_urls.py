from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import *


class AccountsUrlsTestCase(SimpleTestCase):

    def test_login_urls(self):
        url = reverse('accounts:login')
        resolved_view = resolve(url).func
        self.assertEqual(resolved_view.view_class, Login)

    def test_logout_urls(self):
        url = reverse('accounts:logout')
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.func.view_class, Logout)

    def test_change_password_urls(self):
        url = reverse('accounts:change_password')
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.func.view_class, ChangePassword)

    def test_change_password_done_urls(self):
        url = reverse('accounts:change_password_done')
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.func.view_class, ChangePasswordDone)

    def test_password_reset(self):
        url = reverse('accounts:password_reset')
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.func.view_class, PasswordReset)

    def test_password_reset_done(self):
        url = reverse('accounts:password_reset_done')
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.func.view_class, PasswordResetDone)

    def test_password_reset_confirm(self):
        url = reverse('accounts:password_reset_confirm', args=['jhbfdhj', 'jdsjvdds'])
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.func.view_class, PasswordResetConfirm)

    def test_password_reset_complete(self):
        url = reverse('accounts:password_reset_complete')
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.func.view_class, PasswordResetComplete)

    def test_signup_urls(self):
        url = reverse('accounts:signup')
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.func, signup)

    def test_profile_urls(self):
        url = reverse('accounts:profile')
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.func, profile)

    def test_profile_change_urls(self):
        url = reverse('accounts:profile_change')
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.func, profile_change)