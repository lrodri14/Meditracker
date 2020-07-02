from django.test import TestCase, Client
from django.urls import reverse, reverse_lazy
from ..views import *


class TestAccountsViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('accounts:login')
        self.logout_url = reverse('accounts:logout')
        self.change_password_url = reverse('accounts:change_password')
        self.change_password_done_url = reverse('accounts:change_password_done')
        self.password_reset_url = reverse('accounts:password_reset')
        self.password_reset_done_url = reverse('accounts:password_reset_done')
        self.password_reset_confirm_url = reverse('accounts:password_reset_confirm', args=['00000', '00000'])
        self.password_reset_complete_url = reverse('accounts:password_reset_complete')
        self.signup_url = reverse('accounts:signup')
        self.profile_url = reverse('accounts:profile')
        self.profile_change_url = reverse('accounts:profile_change')

    def test_login_view(self):
        response = self.client.get(self.login_url, follow=True)
        c = self.client.login(username='aaaaa', password='aaaaa')
        if c:
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'accounts/login.html')
            self.assertRedirects(expected_url=reverse('home:home'), response=response)

    def test_logout_url(self):
        response = self.client.get(self.logout_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(expected_url=reverse('main:main'), response=response)

    def test_change_password(self):
        c = self.client.login(username='lrodri14', password='bmwm3e46')
        response = self.client.get(self.change_password_url, follow=True)
        if c:
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed('accounts/change_password.html')
            self.assertRedirects(expected_url=reverse('accounts:change_password_done'), response=response)

    def test_change_password_done(self):
        c = self.client.login(username='lrodri14', password='bmwm3e46')
        if c:
            response = self.client.get(self.change_password_done_url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed('accounts/change_password_done.html')

    def test_password_reset(self):
        response = self.client.get(self.password_reset_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/password_reset.html')

    def test_password_reset_confirm(self):
        response = self.client.get(reverse('accounts:password_reset_confirm', args=['00000','000000']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/password_reset_confirm.html')

    def test_signup(self):
        response = self.client.get(reverse('accounts:signup'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/signup.html')

    def test_profile(self):
        response = self.client.get(reverse('accounts:profile'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('accounts/profile.html')
        c = self.client.login(username='aaaa', password='aaaaa')
        if c:
            self.assertRedirects(response=response, expected_url=reverse('accounts:profile'))
        print(response.redirect_chain)

    def test_profile_change(self):
        c = self.client.login(username='aaaa', password='aaaaa')
        if c:
            response = self.client.get(reverse('accounts:profile_change'))
            self.assertRedirects(response=response, expected_url=reverse('accounts:profile'))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed('accounts/profile_change.html')
