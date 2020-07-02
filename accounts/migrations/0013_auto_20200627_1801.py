# Generated by Django 2.2.13 on 2020-06-27 18:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20200625_0614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='roll',
            field=models.CharField(choices=[('Doctor', 'Doctor'), ('Assistant', 'Assistant')], help_text='Choose the roll you will acquire in this account.', max_length=25, verbose_name='Roll'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='speciality',
            field=models.CharField(blank=True, choices=[('ALLERGY & IMMUNOLOGY', 'ALLERGY & IMMUNOLOGY'), ('ANESTHESIOLOGY', 'ANESTHESIOLOGY'), ('DERMATOLOGY', 'DERMATOLOGY'), ('DENTIST', 'DENTIST'), ('DIAGNOSTIC RADIOLOGY', 'DIAGNOSTIC RADIOLOGY'), ('EMERGENCY MEDICINE', 'EMERGENCY MEDICINE'), ('FAMILY MEDICINE', 'FAMILY MEDICINE'), ('INTERNAL MEDICINE', 'INTERNAL MEDICINE'), ('MEDICAL GENETICS', 'MEDICAL GENETICS'), ('NEUROLOGY', 'NEUROLOGY'), ('NUCLEAR MEDICINE', 'NUCLEAR MEDICINE'), ('OBSTETRICS AND GYNECOLOGY', 'OBSTETRICS AND GYNECOLOGY'), ('OPHTHALMOLOGY', 'OPHTHALMOLOGY'), ('PATHOLOGY', 'PATHOLOGY'), ('PEDIATRICS', 'PEDIATRICS'), ('PHYSICAL MEDICINE & REHABILITATION', 'PHYSICAL MEDICINE & REHABILITATION'), ('PREVENTIVE MEDICINE', 'PREVENTIVE MEDICINE'), ('PSYCHIATRY', 'PSYCHIATRY'), ('RADIATION ONCOLOGY', 'RADIATION ONCOLOGY'), ('SURGERY', 'SURGERY'), ('UROLOGY', 'UROLOGY')], help_text='If your roll is (A, Assistant), leave this field blank.', max_length=100, verbose_name='Speciality'),
        ),
        migrations.AlterField(
            model_name='usersprofile',
            name='gender',
            field=models.CharField(choices=[('Masculine', 'Masculine'), ('Femenine', 'Femenine'), ('Undefined', 'Undefined')], max_length=25, null=True, verbose_name='gender'),
        ),
        migrations.AlterField(
            model_name='usersprofile',
            name='location',
            field=models.CharField(choices=[('Honduras', 'Honduras')], help_text='Provide your location', max_length=100, null=True, verbose_name='location'),
        ),
        migrations.AlterField(
            model_name='usersprofile',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]