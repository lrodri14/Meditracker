from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):

    ROLL_CHOICES = (
        ('Doctor', 'Doctor'),
        ('Assistant', 'Assistant'),
    )

    SPECIALITY_CHOICES = (
        ('ALLERGY & IMMUNOLOGY', 'ALLERGY & IMMUNOLOGY'),
        ('ANESTHESIOLOGY', 'ANESTHESIOLOGY'),
        ('DERMATOLOGY', 'DERMATOLOGY'),
        ('DENTIST', 'DENTIST'),
        ('DIAGNOSTIC RADIOLOGY', 'DIAGNOSTIC RADIOLOGY'),
        ('EMERGENCY MEDICINE', 'EMERGENCY MEDICINE'),
        ('FAMILY MEDICINE', 'FAMILY MEDICINE'),
        ('INTERNAL MEDICINE', 'INTERNAL MEDICINE'),
        ('MEDICAL GENETICS', 'MEDICAL GENETICS'),
        ('NEUROLOGY', 'NEUROLOGY'),
        ('NUCLEAR MEDICINE', 'NUCLEAR MEDICINE'),
        ('OBSTETRICS AND GYNECOLOGY', 'OBSTETRICS AND GYNECOLOGY'),
        ('OPHTHALMOLOGY', 'OPHTHALMOLOGY'),
        ('PATHOLOGY', 'PATHOLOGY'),
        ('PEDIATRICS', 'PEDIATRICS'),
        ('PHYSICAL MEDICINE & REHABILITATION', 'PHYSICAL MEDICINE & REHABILITATION'),
        ('PREVENTIVE MEDICINE', 'PREVENTIVE MEDICINE'),
        ('PSYCHIATRY', 'PSYCHIATRY'),
        ('RADIATION ONCOLOGY', 'RADIATION ONCOLOGY'),
        ('SURGERY', 'SURGERY'),
        ('UROLOGY', 'UROLOGY'),
    )

    roll = models.CharField('Roll',max_length=25, blank=False, help_text='Choose the roll you will acquire in this account.', choices=ROLL_CHOICES)
    speciality = models.CharField('Speciality', max_length=100, blank=True, help_text='If your roll is (A, Assistant), leave this field blank.' , choices=SPECIALITY_CHOICES)

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
        ('Honduras', 'Honduras'),
    )

    ORIGIN_CHOICES = (
        ('Honduras', 'Honduras'),
    )

    user = models.OneToOneField(CustomUser, blank=True, null=True, on_delete=models.CASCADE, verbose_name='user', related_name='profile')
    profile_pic = models.ImageField('profile picture', blank=True, null=True, help_text='Let us see you! Upload a profile picture', upload_to='accounts/profile_pictures')
    phone_number = models.CharField('phone number', max_length=15, null=True, blank=True, help_text='Provide your phone number')
    bio = models.TextField('biography', blank=True, null=True, help_text='Let us know about you')
    birth_date = models.DateField('birth date', blank=True, null=True,)
    gender = models.CharField('gender', max_length=25, blank=False, null=True, choices=GENDER_CHOICES)
    origin = models.CharField('origin', max_length=50, blank=False, null=True, choices=ORIGIN_CHOICES)
    location = models.CharField('location', max_length=100, blank=False, null=True, choices=LOCATION_CHOICES, help_text='Provide your location')
    address = models.TextField('address', max_length=200, blank=False, null=True, help_text='Provide your exact address')

    class Meta:
        ordering = ['user']
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return str(self.user) + ' ' + 'Profile Information'
