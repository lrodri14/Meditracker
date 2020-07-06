from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from ..views import *


class TestPatientUrls(TestCase):

    def test_patient_list_url(self):
        url = reverse('patients:patients')
        resolved_url = resolve(url)
        self.assertEqual(resolved_url.func, patients)

    def test_patient_add_url(self):
        url = reverse('patients:add_patient')
        resolve_url = resolve(url)
        self.assertEqual(resolve_url.func, add_patient)

    def test_patient_update_url(self):
        url = reverse('patients:patients_update', kwargs={'pk': 1})
        resolve_url = resolve(url)
        self.assertEqual(resolve_url.func, patient_update)

    def test_patient_details_url(self):
        url = reverse('patients:patients_details', kwargs={'pk': 1})
        resolve_url = resolve(url)
        self.assertEqual(resolve_url.func, patient_details)

    def test_patient_delete_url(self):
        url = reverse('patients:patients_delete', kwargs={'pk': 1})
        resolve_url = resolve(url)
        self.assertEqual(resolve_url.func, patient_delete)