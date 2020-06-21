from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):

    ROLL_CHOICES = (
        ('D', 'Doctor'),
        ('A', 'Assistant'),
    )

    SPECIALITY_CHOICES = (
        ('A&I', 'ALLERGY & IMMUNOLOGY'),
        ('A', 'ANESTHESIOLOGY'),
        ('DM', 'DERMATOLOGY'),
        ('DT', 'DENTIST'),
        ('DR', 'DIAGNOSTIC RADIOLOGY'),
        ('EM', 'EMERGENCY MEDICINE'),
        ('FM', 'FAMILY MEDICINE'),
        ('IM', 'INTERNAL MEDICINE'),
        ('MG', 'MEDICAL GENETICS'),
        ('NEU', 'NEUROLOGY'),
        ('NM', 'NUCLEAR MEDICINE'),
        ('OG', 'OBSTETRICS AND GYNECOLOGY'),
        ('OP', 'OPHTHALMOLOGY'),
        ('PT', 'PATHOLOGY'),
        ('PD', 'PEDIATRICS'),
        ('PMR', 'PHYSICAL MEDICINE & REHABILITATION'),
        ('PM', 'PREVENTIVE MEDICINE'),
        ('PS', 'PSYCHIATRY'),
        ('RO', 'RADIATION ONCOLOGY'),
        ('S', 'SURGERY'),
        ('U', 'UROLOGY'),
    )

    roll = models.CharField('Roll',max_length=25, blank=False, help_text='Choose the roll you will acquire in this account.', choices=ROLL_CHOICES)
    speciality = models.CharField('Speciality', max_length=100, blank=True, help_text='If your roll is (A, Assistant), leave this field blank.' , choices=SPECIALITY_CHOICES)

class UserProfile(models.Model):

    GENDER_CHOICES = (
        ('M', 'Masculine'),
        ('F', 'Femenine'),
        ('U', 'Undefined')
    )

    LOCATION_CHOICES = (
        ('H', 'Honduras'),
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, verbose_name='user')
    profile_pic = models.ImageField('profile picture', null=True)
    bio = models.TextField('biography', blank=True, help_text='Let us know about you')
    birth_date = models.DateField('birth date')
    gender = models.CharField('gender', max_length=25, blank=False, choices=GENDER_CHOICES)
    location = models.CharField('location', max_length=100, blank=False, choices=LOCATION_CHOICES, help_text='Provide your location')

    class Meta:
        ordering = ['user']
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
