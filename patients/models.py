"""
    This models.py file contains all the models needed to perform any data related process in the Patients App.
    It is composed of 6 models.
"""

from django.apps import apps
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
user = get_user_model()
# Create your models here.

# Patients Model


class Patient(models.Model):

    """
        DOCSTRING:
        The Patient class inherits from the models.Model class, this model is used to add Patients to the Patient App,
        there are four tuple choices: GENDER_CHOICES for selection of the patient's gender, CIVIL_STATUS_CHOICES for
        selection of the patient's civil status, PROCEDENCE_CHOICES for selection of the patient's procedence and,
        RESIDENCE_CHOICES for selection of the patient's residence, this class has an age() method which returns the
        age of the patient based on the self.birthday field, it also rewrites the save() method, titling the self.first-
        name and last-name fields, lastly it contains its own dunder __str__ method, which returns the patient's full name.
    """

    GENDER_CHOICES = (
        ('F', 'Femenine'),
        ('M', 'Masculine'),
        ('O', 'Other'),
    )

    CIVIL_STATUS_CHOICES = (
        ('S', 'Single'),
        ('M', 'Married'),
        ('W', 'Widowed'),
        ('D', 'Divorced'),
        ('SP', 'Separated'),
    )

    PROCEDENCE_CHOICES = (
        ('HND', 'Honduras'),
    )

    RESIDENCE_CHOICES = (
        ('HND', 'Honduras'),
    )

    id_number = models.CharField('ID Number', max_length=20, null=True, blank=True,
                                 help_text='Provide you ID Card Number')
    first_names = models.CharField("Patient's Name", max_length=50, null=False, blank=False,
                                help_text="Patient's Name")
    last_names = models.CharField("Patient's Last Name", max_length=50, null=False, blank=False,
                                 help_text="Patient's Last Name")
    gender = models.CharField("Patient's Gender", max_length=20, null=True, blank=False, help_text='Gender', choices=GENDER_CHOICES)
    birthday = models.DateField("Patient's Birthday", help_text="Patients date of birth")
    phone_number = models.CharField('Phone Number', max_length=20, blank=True, null=True, help_text='Phone Number')
    email = models.EmailField("Patient's Email", null=True, blank=True, help_text='Email')
    civil_status = models.CharField(max_length=12, choices=CIVIL_STATUS_CHOICES)
    origin = models.CharField(max_length=50, choices=PROCEDENCE_CHOICES)
    residence = models.CharField(max_length=50, choices=RESIDENCE_CHOICES)
    created_by = models.ForeignKey(user, on_delete=models.CASCADE, blank=False, null=True,
                                   help_text='User who created this patient', verbose_name='created_by',
                                   related_name='creator')

    def age(self):
        today = timezone.localtime(timezone.now())
        age = today.date() - self.birthday
        return int(age.days / 365.25)

    def __str__(self):
        return self.first_names + ' ' + self.last_names

    def save(self, *args, **kwargs):
        self.first_names = self.first_names.title()
        self.last_names = self.last_names.title()
        super(Patient, self).save(*args, **kwargs)

# Insurance Companies Model


class InsuranceCarrier(models.Model):
    """
        DOCSTRING:
        The InsuranceCarrier class inherits from the models.Model class, and is used to create InsuranceCarriers instances,
        an ORIGIN_CHOICES tuple is defined for the country field choices, a class META is set to define the
        unique_together class attribute to ['company', 'created_by'], the save() method has been overwritten
        to title the self.company field, and lastly it contains its own __str__ dunder method.
    """
    ORIGIN_CHOICES = (
        ('HND', 'Honduras'),
        ('NIC', 'Nicaragua'),
    )

    company = models.CharField('company', max_length=100, blank=False, null=False, help_text='Insurance Carrier')
    country = models.CharField('country', max_length=100, blank=False, null=True, help_text='Insurance Carrier origin',
                               choices=ORIGIN_CHOICES, default=None)
    created_by = models.ForeignKey(user, on_delete=models.CASCADE, blank=False, null=True, help_text='Who created this insurance carrier', verbose_name='created_by', related_name='Author')

    class Meta:
        unique_together = ['company', 'created_by']

    def __str__(self):
        return self.company

    def save(self, *args, **kwargs):
        self.company = self.company.title()
        super(InsuranceCarrier, self).save(*args, **kwargs)

    def operative(self, current_user):
        insurance_information_list = InsuranceInformation.objects.filter(patient__created_by=current_user)
        if insurance_information_list:
            for insurance_information in insurance_information_list:
                if insurance_information.insurance_carrier == self:
                    return True


# Patients Insurance Information


class InsuranceInformation(models.Model):
    """
        DOCSTRING:
        The InsuranceCarrierInformation class inherits from the models.Model class, and is used to create Insurance-
        CarriersInformation instances, an INSURANCE_TYPE_CHOICES tuple is defined for the type_of_insurance field
        choices, and lastly it contains its own __str__ dunder method.
    """
    INSURANCE_TYPE_CHOICES = (
        ('MEDICAL', 'Medical'),
    )
    insurance_carrier = models.ForeignKey(InsuranceCarrier, on_delete=models.CASCADE, blank=True, null=True,
                                             verbose_name='insurance carrier', related_name='insurance')
    type_of_insurance = models.CharField('insurance type', max_length=50, blank=True, null=True,
                                         help_text='Type of insurance', choices=INSURANCE_TYPE_CHOICES)
    expiration_date = models.DateField('insurance date expiration', help_text='insurance date expiration')
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, blank=True, null=True, verbose_name='insurance owner', related_name='insurance')

    def __str__(self):
        return str(self.patient) + "'s" + ' ' + 'Insurance Information'

# Allergies Information


class Allergy(models.Model):
    """
        DOCSTRING:
        The Allergies class inherits from the models.Model class, and is used to create Allergies instances,
         a class META is set to define the unique_together class attribute to ['allergy_type', 'created_by'],
        the save() method has been overwritten to title the self.allergy_type field, and lastly it contains
        its own __str__ dunder method.
    """
    allergy_type = models.CharField('allergy', max_length=100, null=False, blank=False, help_text='Allergy Type')
    created_by = models.ForeignKey(user, blank=False, on_delete=models.CASCADE, null=True,
                                      help_text='User by who this allergy was created', related_name='user')

    class Meta:
        unique_together = ['allergy_type', 'created_by']

    def __str__(self):
        return self.allergy_type

    def save(self, *args, **kwargs):
        self.allergy_type = self.allergy_type.title()
        super(Allergy, self).save(*args, **kwargs)

    def operative(self, current_user):
        allergy_information_list = AllergyInformation.objects.filter(patient__created_by=current_user)
        if allergy_information_list:
            for allergy_information in allergy_information_list:
                if allergy_information.allergy_type == self:
                    return True

# Patient Allergies Information


class AllergyInformation(models.Model):
    """
        DOCSTRING:
        The AllergiesInformation class inherits from the models.Model class, and is used to create Allergies-
        Information instances, it rewrote the save() method to capitalize the self.about field in the model,
        and lastly it contains its own __str__ dunder method.
    """
    allergy_type = models.ForeignKey(Allergy, on_delete=models.CASCADE, null=True, blank=True, verbose_name='allergy type',
                                        help_text='Allergy type of the patient', related_name='allergy')
    about = models.TextField('about allergy', help_text='Tell us about what you suffer', blank=True, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=False, null=True, verbose_name='Patient',
                                                                                            related_name='allergies')

    def __str__(self):
        return str(self.patient) + "'s" + ' ' + 'Allergies Information'

    def save(self, *args, **kwargs):
        self.about = self.about.capitalize()
        super(AllergyInformation, self).save(*args, **kwargs)

# Patient Antecedents Information


class Antecedent(models.Model):
    """
        DOCSTRING:
        The Antecedents class inherits from the models.Model class, and is used to create Antecedents instances,
        it rewrote the save() method to capitalize the self.antecedent and self.info field in the model,
        and lastly it contains its own __str__ dunder method.
    """
    antecedent = models.CharField('antecedent', max_length=150, blank=True, null=True, help_text='Antecedent Type')
    info = models.TextField('antecedent info', blank=True, null=True, help_text='About this antecedent')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=False, null=True, verbose_name='Patient',
                                                                                            related_name='antecedents')

    def __str__(self):
        return str(self.patient) + "'s" + ' ' + 'Antecedents Information'

    def save(self, *args, **kwargs):
        if self.antecedent and self.info:
            self.antecedent = self.antecedent.title()
            self.info = self.info.capitalize()
        super(Antecedent, self).save(*args, **kwargs)


