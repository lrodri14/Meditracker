from django.test import TestCase, Client
from django.shortcuts import reverse

# Create your tests here.


class TestMainView(TestCase):

    def test_main_view(self):
        client = Client()
        response = client.get(reverse('main:main'))
        self.assertEqual(response.status_code, 200)


