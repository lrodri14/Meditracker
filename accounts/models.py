from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):

    ROLL_CHOICES = (
        ('Doctor', 'Doctor'),
        ('Assistant', 'Assistant'),
    )

    SPECIALITY_CHOICES = (
        ('ALLERGY & IMMUNOLOGY', 'Allergy & Immunology'),
        ('ANESTHESIOLOGY', 'Anesthesiology'),
        ('DERMATOLOGY', 'Dermatology'),
        ('DENTIST', 'Dentist'),
        ('DIAGNOSTIC RADIOLOGY', 'Diagnostic Radiology'),
        ('EMERGENCY MEDICINE', 'Emergency Medicine'),
        ('FAMILY MEDICINE', 'Family Medicine'),
        ('INTERNAL MEDICINE', 'Internal Medicine'),
        ('MEDICAL GENETICS', 'Medical Genetics'),
        ('NEUROLOGY', 'Neurology'),
        ('NUCLEAR MEDICINE', 'Nuclear Medicine'),
        ('OBSTETRICS AND GYNECOLOGY', 'Obstetrics & Gynechology'),
        ('OPHTHALMOLOGY', 'Ophthalmolgy'),
        ('PATHOLOGY', 'Pathology'),
        ('PEDIATRICS', 'Pediatrics'),
        ('PHYSICAL MEDICINE & REHABILITATION', 'Physical Medicine & Rehabilitation'),
        ('PREVENTIVE MEDICINE', 'Preventive Medicine'),
        ('PSYCHIATRY', 'Psychiatry'),
        ('RADIATION ONCOLOGY', 'Radiation Oncology'),
        ('SURGERY', 'Surgery'),
        ('UROLOGY', 'Urology'),
    )
    email = models.EmailField(blank=False, unique=True)
    roll = models.CharField('Roll', max_length=25, blank=False, help_text='Choose the roll you will acquire in this account.', choices=ROLL_CHOICES)
    speciality = models.CharField('Speciality', max_length=100, blank=True, help_text='If your roll is (A, Assistant), leave this field blank.', choices=SPECIALITY_CHOICES)

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.title()
        self.last_name = self.last_name.title()
        created = not self.pk
        super(CustomUser, self).save(*args, **kwargs)
        if created:
            UsersProfile.objects.create(user=self)


class UsersProfile(models.Model):

    GENDER_CHOICES = (
        ('Masculine', 'Masculine'),
        ('Femenine', 'Femenine'),
        ('Undefined', 'Undefined')
    )

    LOCATION_CHOICES = (
        ('HND', 'Honduras'),
    )

    ORIGIN_CHOICES = (
        ('HND', 'Honduras'),
    )

    user = models.OneToOneField(CustomUser, blank=True, null=True, on_delete=models.CASCADE, verbose_name='user', related_name='profile')
    profile_pic = models.ImageField('Profile Picture', blank=True, null=True, upload_to='accounts/profile_pictures')
    background_pic = models.ImageField('Background Picture', blank=True, null=True, upload_to='accounts/background_pictures')
    phone_number = models.CharField('Phone Number', max_length=15, null=True, blank=True, help_text='Provide your phone number')
    bio = models.TextField('Biography', blank=True, null=True, help_text='Let us know about you')
    birth_date = models.DateField('Birth Date', blank=True, null=True,)
    gender = models.CharField('Gender', max_length=25, blank=False, null=True, choices=GENDER_CHOICES)
    origin = models.CharField('Origin', max_length=50, blank=False, null=True, choices=ORIGIN_CHOICES)
    location = models.CharField('Location', max_length=100, blank=False, null=True, choices=LOCATION_CHOICES, help_text='Provide your location')
    address = models.TextField('Address', max_length=200, blank=False, null=True, help_text='Provide your exact address')
    tzone = models.CharField('Timezone', max_length=40, blank=False, null=True, help_text='Provide your timezone')
    contacts = models.ManyToManyField(to=CustomUser, blank=True, help_text='Contacts List')

    class Meta:
        ordering = ['user']
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return str(self.user) + ' - ' + 'User Profile'


class MailingCredential(models.Model):
    smtp_server = models.CharField("SMTP Server", max_length=100, blank=True, null=True, help_text="Provide the SMTP Server", default="")
    port = models.IntegerField("Port", blank=True, null=True, help_text="Provide the port used by your server")
    email = models.EmailField("Email", blank=True, null=True, help_text="Provide your email")
    password = models.CharField("Password", max_length=254, blank=True, null=True, help_text="Provide your password")
    use_tls = models.BooleanField("Use TLS? (Recommended)", default=False)
    user = models.OneToOneField(CustomUser, blank=True, null=True, related_name="mailing_credentials", on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Mailing Credential'
        verbose_name_plural = 'Mailing Credentials'

    def __str__(self):
        return str(self.user) + ' - ' + 'Mailing Credentials'
