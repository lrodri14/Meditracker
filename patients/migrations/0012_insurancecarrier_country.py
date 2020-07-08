# Generated by Django 2.2.13 on 2020-07-07 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0011_remove_patient_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='insurancecarrier',
            name='country',
            field=models.CharField(choices=[('HND', 'Honduras')], default=None, help_text='Insurance Carrier origin', max_length=100, null=True, verbose_name='country'),
        ),
    ]
