# Generated by Django 2.2.13 on 2020-11-23 17:16

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('patients', '0041_auto_20201023_1635'),
        ('appointments', '0038_auto_20201123_1600'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='consults',
            unique_together={('created_by', 'patient', 'datetime', 'medical_status')},
        ),
    ]
