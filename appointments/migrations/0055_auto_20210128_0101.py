# Generated by Django 2.2.13 on 2021-01-28 01:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0054_auto_20210128_0047'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MedicalExam',
            new_name='MedicalTestResult',
        ),
        migrations.AlterModelOptions(
            name='medicaltestresult',
            options={'verbose_name': 'Medical Test Result', 'verbose_name_plural': 'Medical Test Results'},
        ),
    ]