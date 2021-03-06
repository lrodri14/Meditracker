# Generated by Django 2.2.13 on 2020-06-21 14:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='roll',
            field=models.CharField(choices=[('D', 'Doctor'), ('A', 'Assistant')], help_text='Choose the roll you will acquire in this account.', max_length=25, verbose_name='Roll'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='speciality',
            field=models.CharField(blank=True, choices=[('A&I', 'ALLERGY & IMMUNOLOGY'), ('A', 'ANESTHESIOLOGY'), ('DM', 'DERMATOLOGY'), ('DT', 'DENTIST'), ('DR', 'DIAGNOSTIC RADIOLOGY'), ('EM', 'EMERGENCY MEDICINE'), ('FM', 'FAMILY MEDICINE'), ('IM', 'INTERNAL MEDICINE'), ('MG', 'MEDICAL GENETICS'), ('NEU', 'NEUROLOGY'), ('NM', 'NUCLEAR MEDICINE'), ('OG', 'OBSTETRICS AND GYNECOLOGY'), ('OP', 'OPHTHALMOLOGY'), ('PT', 'PATHOLOGY'), ('PD', 'PEDIATRICS'), ('PMR', 'PHYSICAL MEDICINE & REHABILITATION'), ('PM', 'PREVENTIVE MEDICINE'), ('PS', 'PSYCHIATRY'), ('RO', 'RADIATION ONCOLOGY'), ('S', 'SURGERY'), ('U', 'UROLOGY')], help_text='If your roll is (A, Assistant), leave this field blank.', max_length=100, verbose_name='Speciality'),
        ),
        migrations.CreateModel(
            name='UsersProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', models.ImageField(null=True, upload_to='', verbose_name='profile picture')),
                ('bio', models.TextField(blank=True, help_text='Let us know about you', verbose_name='biography')),
                ('birth_date', models.DateField(verbose_name='birth date')),
                ('gender', models.CharField(choices=[('M', 'Masculine'), ('F', 'Femenine'), ('U', 'Undefined')], max_length=25, verbose_name='gender')),
                ('location', models.CharField(choices=[('H', 'Honduras')], help_text='Provide your location', max_length=100, verbose_name='location')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'User Profile',
                'verbose_name_plural': 'User Profiles',
                'ordering': ['user'],
            },
        ),
    ]
