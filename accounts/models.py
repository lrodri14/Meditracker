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

    roll = models.CharField('Roll',max_length=25, blank=False, help_text='*Required', choices=ROLL_CHOICES)
    speciality = models.CharField('Speciality', max_length=100, blank=True, choices=SPECIALITY_CHOICES, help_text='If your roll is (A, Assistant), leave this field blank.')


class Profile:
    GENDER_CHOICES = (
        ('M', 'Masculine'),
        ('F', 'Femenine'),
        ('U', 'Undefined'),
    )
    user = models.OneToOneField(get_user_model(),on_delete=models.CASCADE,verbose_name='User')
    profile_pic = models.ImageField('Profile Picture', null=True)
    gender = models.CharField('Gender', max_length=25, blank=False, choices=GENDER_CHOICES)
    birth_date = models.DateField('Birth Date', null=True)
    # country = models.CharField('Country', max_length=100, choices=COUNTRY_CHOICES)

