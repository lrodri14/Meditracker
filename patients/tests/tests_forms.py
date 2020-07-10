from ..forms import *
from django.test import SimpleTestCase, TestCase
from django.utils import timezone
from ..models import InsuranceCarrier
from django.contrib.auth import get_user_model


class TestPatientForm(TestCase):

    def test_patient_form_is_valid(self):
        patient = PatientForm(data={
            'id_number': 1709200001231,
            'first_names': 'luis',
            'last_names': 'rodriguez',
            'birthday': timezone.datetime(year=2000, month=9, day=4),
            'phone_number': 33905511,
            'civil_status': 'S',
            'origin': 'HND',
            'residence': 'HND',
        })

        self.assertTrue(patient.is_valid())

    def test_patient_form_is_invalid(self):
        patient = PatientForm(data={
            'id_number': 1709200001231,
            'first_names': 'luis',
            'last_names': 'rodriguez',
            'birthday': None,
            'phone_number': 33905511,
            'civil_status': None,
            'origin': None,
            'residence': None,
        })

        self.assertFalse(patient.is_valid())
        self.assertEquals(len(patient.errors), 4)


class TestInsuranceCarrierForm(TestCase):

    def test_insurance_carrier_form_is_valid(self):
        insurance_carrier = InsuranceCarrierForm(data={
            'company': 'lafise',
            'country': 'NIC'
        })
        self.assertTrue(insurance_carrier.is_valid())

    def test_insurance_carrier_form_is_invalid(self):
        insurance_carrier = InsuranceCarrierForm(data={
            'company': None
        })
        self.assertEquals(len(insurance_carrier.errors), 2)

#
# class TestInsuranceInformationForm(TestCase):
#
#     longMessage = True
#
#     def setUp(self):
#         self.insurance = InsuranceCarrier.objects.create(
#             company='lafise'
#         )
#
#     def test_insurance_information_form_is_valid(self):
#         insurance_form = InsuranceInformationForm(data={
#             'insurance_carrier': self.insurance,
#             'type_of_insurance': 'MEDICAL',
#             'expiration_date': timezone.now()
#         })
#
#         self.assertTrue(insurance_form.is_valid())
#
#     def test_insurance_information_form_is_invalid(self):
#         insurance_form = InsuranceInformationForm(data={
#             'insurance_carrier': 'lafise',
#             'type_of_insurance': 'MEDICAL',
#             'expiration_date': timezone.now()
#         })
#
#         self.assertFalse(insurance_form.is_valid())


class TestAllergiesForm(SimpleTestCase):

    def test_allergies_form_is_valid(self):
        allergy = AllergiesForm(data={
            'allergy_type': 'dust',
            'created_by': 'user'
        })

        self.assertTrue(allergy.is_valid())

    def test_allergies_form_is_invalid(self):
        allergy = AllergiesForm(data={
            'allergy_type': None
        })

        self.assertFalse(allergy.is_valid())

#
# class TestAllergiesInformationForm(TestCase):
#
#     def setUp(self):
#         self.patient = Patient.objects.create(
#             id_number=1709200001231,
#             first_names='adrian luis',
#             last_names='perez rodriguez',
#             birthday=timezone.now(),
#             phone_number=33099408,
#             civil_status='M',
#             origin='HND',
#             residence='HND',
#         )
#
#         self.allergy = Allergies.objects.create(
#             allergy_type='dust'
#         )
#
#     def test_allergies_information_form_is_valid(self):
#         allergy = AllergiesInformationForm(data={
#             'allergy_type': self.allergy,
#             'about': 'allergic to everything that retains dust',
#         })
#
#         self.assertTrue(allergy.is_valid())
#
#     def test_allergies_information_form_is_invalid(self):
#         allergy = AllergiesInformationForm(data={
#             'allergy_type': self.allergy,
#             'about': 'allergic to everything that retains dust',
#         })
#
#         self.assertFalse(allergy.is_valid())


class TestAntecedentForm(SimpleTestCase):

    def test_antecedents_form_is_valid(self):
        antecedent = AntecedentForm(data={
            'antecedent':'heart problems',
            'info': 'hereditary heart problems'
        })
        
        self.assertTrue(antecedent.is_valid())

    def test_antecedents_form_is_invalid(self):
        antecedent = AntecedentForm(data={
            'antecedent': '$$$$'*151,
            'info': '$$$$',
        })

        self.assertFalse(antecedent.is_valid())
        self.assertEquals(len(antecedent.errors), 1)


