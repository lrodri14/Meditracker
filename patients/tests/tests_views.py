from django.test import TestCase, Client
from ..models import Patient
from django.utils import timezone
from django.urls import reverse
from ..views import *
from ..forms import PatientForm, AllergiesInformationForm, AntecedentForm, InsuranceInformationForm


class TestPatientsView(TestCase):

    def setUp(self):
        self.client = Client()
        for x in range(0, 10):
            Patient.objects.create(
                id_number=1709200001231,
                first_names='luis',
                last_names='rodriguez',
                birthday=timezone.now(),
                phone_number='33905511',
                civil_status='S',
                origin='HND',
                residence='HND'
            )
        self.patient_url = reverse('patients:patients')

    def test_patients_view_response(self):
        response = self.client.get(self.patient_url)
        context = 0
        for patient in response.context['patients']:
            context += 1
        self.assertEqual(response.status_code, 200)
        self.assertEqual(context, 10)

    def test_patients_template_used(self):
        response = self.client.get(self.patient_url)
        self.assertTemplateUsed(response, 'patients/patients.html')

    def test_patients_view_context(self):
        response = self.client.get(self.patient_url)
        context = 0
        for patient in response.context['patients']:
            context += 1
        self.assertEqual(context, 10)


class TestAddPatientView(TestCase):

    def setUp(self):
        self.client = Client()
        self.add_patient_url = reverse('patients:add_patient')
        self.patient_form = PatientForm
        self.allergies_form = AllergiesInformationForm
        self.insurance_form = InsuranceInformationForm
        self.antecedents_form = AntecedentForm

    def test_add_patients_response(self):
        response = self.client.get(self.add_patient_url)
        self.assertEqual(response.status_code, 200)

    def test_add_patients_context(self):
        response = self.client.get(self.add_patient_url)
        self.assertEqual(response.context['patient_form'], self.patient_form)
        self.assertEqual(response.context['allergies_form'], self.allergies_form)
        self.assertEqual(response.context['insurance_form'], self.insurance_form)
        self.assertEqual(response.context['antecedents_form'], self.antecedents_form)

    def test_add_patients_template_used(self):
        response = self.client.get(self.add_patient_url)
        self.assertTemplateUsed(response, 'patients/add_patient.html')


class TestPatientDetailsView(TestCase):

    def setUp(self):
        self.client = Client()
        Patient.objects.create(
            id_number=1709200001231,
            first_names='luis',
            last_names='rodriguez',
            birthday=timezone.now(),
            phone_number='33905511',
            civil_status='S',
            origin='HND',
            residence='HND'
        )
        self.patient = Patient.objects.get(first_names='luis'.title())
        self.patient_details_url = reverse('patients:patients_details', kwargs={'pk':self.patient.pk})

    def test_patient_details_response(self):
        response = self.client.get(self.patient_details_url)
        self.assertEqual(response.status_code, 200)

    def test_patient_details_context(self):
        response = self.client.get(self.patient_details_url)
        self.assertTrue(response.context['patient'], self.patient)


class TestPatientDelete(TestCase):

    def setUp(self):
        self.client = Client()
        Patient.objects.create(
            id_number=1709200001231,
            first_names='luis',
            last_names='rodriguez',
            birthday=timezone.now(),
            phone_number='33905511',
            civil_status='S',
            origin='HND',
            residence='HND'
        )
        self.patient = Patient.objects.get(first_names='luis'.title())
        self.patient_delete_url = reverse('patients:patients_delete', kwargs={'pk': self.patient.pk})

    def test_patient_delete_response(self):
        response = self.client.get(self.patient_delete_url)
        self.assertEquals(response.status_code, 200)

    def test_patient_delete_context(self):
        response = self.client.get(self.patient_delete_url)
        self.assertTrue(response.context['patient'], self.patient)

    def test_patient_delete_template(self):
        response = self.client.get(self.patient_delete_url)
        self.assertTemplateUsed(response, 'patients/patients_delete.html')


class TestPatientUpdate(TestCase):

    def setUp(self):
        self.patient = Patient.objects.create(
            id_number=1709200001231,
            first_names='luis',
            last_names='rodriguez',
            birthday=timezone.now(),
            phone_number='33905511',
            civil_status='S',
            origin='HND',
            residence='HND'
        )
        self.insurance_carrier = InsuranceCarrier.objects.create(
            company='Lafise'
        )

        self.insurance_info = InsuranceInformation.objects.create(
            insurance_carrier=self.insurance_carrier,
            type_of_insurance='MEDICAL',
            expiration_date=timezone.now(),
            patient=self.patient
        )

        self.allergy = Allergies.objects.create(
            allergy_type='dust'
        )

        self.allergies_info = AllergiesInformation.objects.create(
            allergy_type=self.allergy,
            about='allergic to everything that retains dust',
            patient=self.patient
        )

        self.antecedents = Antecedents.objects.create(
            antecedent='heart problems',
            info='chronic cardiac problems',
            patient=self.patient
        )

        self.client = Client()
        self.update_patient_url = reverse('patients:patients_update', kwargs={'pk': self.patient.pk})
        self.patient_form = PatientForm(instance=self.patient)
        self.allergies_form = AllergiesInformationForm(instance=self.allergies_info)
        self.insurance_form = InsuranceInformationForm(instance=self.insurance_info)
        self.antecedents_form = AntecedentForm(instance=self.antecedents)

    def test_update_patients_response(self):
        response = self.client.get(self.update_patient_url)
        self.assertEqual(response.status_code, 200)

    def test_update_patients_context(self):
        response = self.client.get(self.update_patient_url)
        self.assertTrue('patient_form' in response.context)
        self.assertTrue('allergies_form' in response.context)
        self.assertTrue('insurance_form' in response.context)
        self.assertTrue('antecedents_form' in response.context)

    def test_update_patients_template_used(self):
        response = self.client.get(self.update_patient_url)
        self.assertTemplateUsed(response, 'patients/patients_update.html')


