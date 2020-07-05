from django.test import SimpleTestCase
from django.urls import reverse, resolve


class TestUrls(SimpleTestCase):

    def test_patient_list_url(self):
        url = reverse('patients:patients')
        print(url)