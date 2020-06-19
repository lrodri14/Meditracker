from django.db import models
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

    roll = models.CharField(max_length=25, blank=True, choices=ROLL_CHOICES)
    speciality = models.CharField(max_length=100, blank=True, choices=SPECIALITY_CHOICES)
