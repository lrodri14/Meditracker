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
        ('M', 'Masculine'),
        ('F', 'Femenine'),
        ('U', 'Undefined')
    )

    LOCATION_CHOICES = (
        ('HN', 'Honduras'),
    )

    user = models.OneToOneField(CustomUser, blank=True, null=True, on_delete=models.CASCADE, verbose_name='user')
    profile_pic = models.ImageField('profile picture', blank=True, null=True, help_text='Let us see you! Upload a profile picture', upload_to='accounts/profile_pictures')
    phone_number = models.CharField('phone number', max_length=15, null=True, blank=True, help_text='Provide your phone number')
    bio = models.TextField('biography', blank=True, null=True, help_text='Let us know about you')
    birth_date = models.DateField('birth date', blank=True, null=True,)
    gender = models.CharField('gender', max_length=25, blank=False, null=True, choices=GENDER_CHOICES)
    location = models.CharField('location', max_length=100, blank=False, null=True, choices=LOCATION_CHOICES, help_text='Provide your location')
    address = models.TextField('address', max_length=200, blank=False, null=True, help_text='Provide your exact address')

    class Meta:
        ordering = ['user']
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return str(self.user) + ' ' + 'Profile Information'
