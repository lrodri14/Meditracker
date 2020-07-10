from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
user = get_user_model()
# Create your models here.

# Patients Model


class Patient(models.Model):
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

    id_number = models.CharField('ID number', max_length=20, null=True, blank=True,
                                 help_text='Provide you ID Card Number')
    first_names = models.CharField('patients name', max_length=50, null=False, blank=False,
                                help_text="Patient's Name")
    last_names = models.CharField('patients last name', max_length=50, null=False, blank=False,
                                 help_text="Patient's Last Name")
    birthday = models.DateTimeField('patients birthday', help_text="Patients date of birth")
    phone_number = models.CharField('phone number', max_length=20, blank=True, null=True, help_text='Phone Number')
    civil_status = models.CharField(max_length=12, choices=CIVIL_STATUS_CHOICES)
    origin = models.CharField(max_length=50, choices=PROCEDENCE_CHOICES)
    residence = models.CharField(max_length=50, choices=RESIDENCE_CHOICES)
    created_by = models.ForeignKey(user, on_delete=models.CASCADE, blank=False, null=True,
                                   help_text='User who created this patient', verbose_name='created_by',
                                   related_name='creator')

    def age(self):
        today = timezone.localtime(timezone.now())
        age = today - self.birthday
        return int(age.days / 365.25)

    def __str__(self):
        return self.first_names + ' ' + self.last_names

    def save(self, *args, **kwargs):
        self.first_names = self.first_names.title()
        self.last_names = self.last_names.title()
        super(Patient, self).save(*args, **kwargs)


# Insurance Companies Model


class InsuranceCarrier(models.Model):

    ORIGIN_CHOICES = (
        ('HND', 'Honduras'),
        ('NIC', 'Nicaragua'),
    )

    company = models.CharField('company', max_length=100, blank=False, null=False, help_text='Insurance Carrier')
    country = models.CharField('country', max_length=100, blank=False, null=True, help_text='Insurance Carrier origin',
                               choices=ORIGIN_CHOICES, default=None)

    class Meta:
        unique_together = ['company', 'country']

    def __str__(self):
        return self.company

    def save(self, *args, **kwargs):
        self.company = self.company.title()
        super(InsuranceCarrier, self).save(*args, **kwargs)


# Patients Insurance Information


class InsuranceInformation(models.Model):
    INSURANCE_TYPE_CHOICES = (
        ('MEDICAL', 'Medical'),
    )
    insurance_carrier = models.OneToOneField(InsuranceCarrier, on_delete=models.CASCADE, blank=True, null=True,
                                             verbose_name='insurance carrier', related_name='insurance', unique=True)
    type_of_insurance = models.CharField('insurance type', max_length=50, blank=True, null=True,
                                         help_text='Type of insurance', choices=INSURANCE_TYPE_CHOICES)
    expiration_date = models.DateField('insurance date expiration', help_text='insurance date expiration')
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, blank=True, null=True,
                                   verbose_name='insurance owner', related_name='insurance')

    def __str__(self):
        return str(self.patient)+ "'s" + ' ' + 'Insurance Information'

# Allergies Information


class Allergies(models.Model):
    allergy_type = models.CharField('allergy', max_length=100, null=False, blank=False, help_text='Allergy Type')
    created_by = models.ForeignKey(user, blank=False, on_delete=models.CASCADE, null=True,
                                      help_text='User by who this allergy was created', related_name='user')

    def __str__(self):
        return self.allergy_type

    def save(self, *args, **kwargs):
        self.allergy_type = self.allergy_type.title()
        super(Allergies, self).save(*args, **kwargs)

    class Meta:
        unique_together = ['allergy_type', 'created_by']

# Patient Allergies Information


class AllergiesInformation(models.Model):
    allergy_type = models.OneToOneField(Allergies, on_delete=models.CASCADE, null=True, blank=True, verbose_name='allergy type',
                                        help_text='Allergy type of the patient', related_name='allergy')
    about = models.TextField('about allergy', help_text='Tell us about what you suffer', blank=True, null=True)
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, blank=False, null=True, verbose_name='Patient',
                                                                                            related_name='allergies')

    def __str__(self):
        return str(self.patient) + "'s" + ' ' + 'Allergies Information'

    def save(self, *args, **kwargs):
        self.about = self.about.capitalize()
        super(AllergiesInformation, self).save(*args, **kwargs)

# Patient Antecedents Information


class Antecedents(models.Model):
    antecedent = models.CharField('antecedent', max_length=150, blank=True, null=True, help_text='Antecedent Type')
    info = models.TextField('antecedent info', blank=True, null=True, help_text='About this antecedent')
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, blank=False, null=True, verbose_name='Patient',
                                                                                            related_name='antecedents')

    def __str__(self):
        return str(self.patient) + "'s" + ' ' + 'Antecedents Information'

    def save(self, *args, **kwargs):
        if self.antecedent and self.info:
            self.antecedent = self.antecedent.title()
            self.info = self.info.capitalize()
        super(Antecedents, self).save(*args, **kwargs)


