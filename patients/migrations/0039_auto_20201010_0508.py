# Generated by Django 2.2.13 on 2020-10-10 05:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0038_auto_20201010_0404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allergiesinformation',
            name='allergy_type',
            field=models.ForeignKey(blank=True, help_text='Allergy type of the patient', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='allergy', to='patients.Allergies', verbose_name='allergy type'),
        ),
    ]
