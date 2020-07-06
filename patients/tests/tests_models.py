from django.test import TestCase
from django.utils import timezone
from ..models import *


class TestPatientModels(TestCase):

    def setUp(self):
        Patient.objects.create(
            id_number=1709200001231,
            first_names='adrian luis',
            last_names='perez rodriguez',
            birthday=timezone.now(),
            phone_number=33099408,
            civil_status='M',
            origin='HND',
            residence='HND',
        )

    def test_patient_model_str(self):
        patient = Patient.objects.get(first_names='adrian luis'.title())
        self.assertEqual(str(patient), 'Adrian Luis Perez Rodriguez')

    def test_patient_model_save(self):
        patient = Patient.objects.get(first_names='adrian luis'.title())
        self.assertEqual(patient.first_names, 'Adrian Luis')
        self.assertEqual(patient.last_names, 'Perez Rodriguez')


class TestInsuranceCarrierModel(TestCase):

    def setUp(self):
        InsuranceCarrier.objects.create(company='ficohsa')

    def test_insurance_carrier_model_str(self):
        insurance_carrier = InsuranceCarrier.objects.get(company='ficohsa'.title())
        self.assertEqual(str(insurance_carrier), 'Ficohsa')

    def test_insurance_carrier_mode_save(self):
        insurance_carrier = InsuranceCarrier.objects.get(company='ficohsa'.title())
        self.assertEqual(insurance_carrier.company, 'Ficohsa')


class TestInsurnaceInformationModel(TestCase):

    def setUp(self):
        Patient.objects.create(
            id_number=1709200001231,
            first_names='adrian luis',
            last_names='perez rodriguez',
            birthday=timezone.now(),
            phone_number=33099408,
            civil_status='M',
            origin='HND',
            residence='HND',
        )
        InsuranceCarrier.objects.create(company='lafise')

    def test_insurance_information_create(self):
        patient = Patient.objects.get(first_names='adrian luis'.title())
        insurance_carrier = InsuranceCarrier.objects.get(company='lafise'.title())
        InsuranceInformation.objects.create(insurance_carrier=insurance_carrier,
                                            type_of_insurance='MEDICAL',
                                            expiration_date=timezone.now(),
                                            patient=patient)

        insurance_info = InsuranceInformation.objects.get(patient=patient)
        self.assertTrue(insurance_info)

    def test_insurance_information_str(self):
        patient = Patient.objects.get(first_names='adrian luis'.title())
        insurance_carrier = InsuranceCarrier.objects.get(company='lafise'.title())
        InsuranceInformation.objects.create(insurance_carrier=insurance_carrier,
                                            type_of_insurance='MEDICAL',
                                            expiration_date=timezone.now(),
                                            patient=patient)

        insurance_info = InsuranceInformation.objects.get(patient=patient)
        self.assertEqual(str(insurance_info), "Adrian Luis Perez Rodriguez's Insurance Information")


class TestAllergiesModel(TestCase):

    def setUp(self):
        Allergies.objects.create(allergy_type='dust')

    def test_allergies_model_save(self):
        allergy = Allergies.objects.get(pk=1)
        self.assertEqual(allergy.allergy_type, 'Dust')

    def test_allergies_model_str(self):
        allergy = Allergies.objects.get(pk=1)
        self.assertEqual(str(allergy), 'Dust')


class TestAllergiesInformationModel(TestCase):

    def setUp(self):
        Patient.objects.create(
            id_number=1709200001231,
            first_names='adrian luis',
            last_names='perez rodriguez',
            birthday=timezone.now(),
            phone_number=33099408,
            civil_status='M',
            origin='HND',
            residence='HND',
        )
        InsuranceCarrier.objects.create(company='lafise')
        Allergies.objects.create(allergy_type='dust')

    def test_allergies_information_str(self):
        allergy_type = Allergies.objects.get(allergy_type='dust'.title())
        patient = Patient.objects.get(first_names='adrian luis'.title())
        allergies_info = AllergiesInformation.objects.create(
            allergy_type=allergy_type,
            about='allergic to things that retain dust',
            patient=patient
        )
        self.assertEqual(str(allergies_info), "Adrian Luis Perez Rodriguez's Allergies Information")

    def test_allergies_information_save(self):
        allergy_type = Allergies.objects.get(allergy_type='dust'.title())
        patient = Patient.objects.get(first_names='adrian luis'.title())
        allergies_info = AllergiesInformation.objects.create(
            allergy_type=allergy_type,
            about='allergic to things that retain dust',
            patient=patient
        )

        self.assertEqual(allergies_info.about, 'Allergic to things that retain dust')


class TestAntecedentsModel(TestCase):

    def setUp(self):
        Patient.objects.create(
            id_number=1709200001231,
            first_names='adrian luis',
            last_names='perez rodriguez',
            birthday=timezone.now(),
            phone_number=33099408,
            civil_status='M',
            origin='HND',
            residence='HND',
        )

    def test_antecedents_model_str(self):
        patient = Patient.objects.get(first_names='adrian luis'.title())
        antecedents = Antecedents.objects.create(
            antecedent='heart problems',
            info='heart illness',
            patient=patient
        )
        self.assertEqual(str(antecedents), "Adrian Luis Perez Rodriguez's Antecedents Information")

    def test_antecedents_model_save(self):
        patient = Patient.objects.get(first_names='adrian luis'.title())
        antecedents = Antecedents.objects.create(
            antecedent='heart problems',
            info='heart illness',
            patient=patient
        )

        self.assertEqual(antecedents.antecedent, antecedents.antecedent.title())
        self.assertEqual(antecedents.info, antecedents.info.capitalize())





