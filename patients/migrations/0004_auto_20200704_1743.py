# Generated by Django 2.2.13 on 2020-07-04 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0003_patient_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allergiesinformation',
            name='about',
            field=models.TextField(blank=True, help_text='Tell us about what you suffer', null=True, verbose_name='about allergy'),
        ),
    ]
