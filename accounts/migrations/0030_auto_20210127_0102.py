# Generated by Django 2.2.13 on 2021-01-27 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0029_auto_20210117_0307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='roll',
            field=models.CharField(choices=[('Doctor', 'Doctor'), ('Assistant', 'Assistant'), ('Patient', 'Patient')], help_text='Choose the roll you will acquire in this account.', max_length=25, verbose_name='Roll'),
        ),
        migrations.AlterField(
            model_name='usersprofile',
            name='birth_date',
            field=models.DateField(blank=True, help_text='Birth date', null=True, verbose_name='Birth Date'),
        ),
        migrations.AlterField(
            model_name='usersprofile',
            name='gender',
            field=models.CharField(choices=[('Masculine', 'Masculine'), ('Femenine', 'Femenine')], max_length=25, null=True, verbose_name='Gender'),
        ),
        migrations.AlterField(
            model_name='usersprofile',
            name='location',
            field=models.CharField(choices=[('AR', 'Argentina'), ('BR', 'Brazil'), ('BZ', 'Belize'), ('CA', 'Canada'), ('CL', 'Chile'), ('CO', 'Colombia'), ('CR', 'Costa Rica'), ('GT', 'Guatemala'), ('HN', 'Honduras'), ('MX', 'Mexico'), ('NI', 'Nicaragua'), ('PA', 'Panama'), ('SV', 'El Salvador'), ('US', 'United States')], help_text='Provide your location', max_length=100, null=True, verbose_name='Location'),
        ),
        migrations.AlterField(
            model_name='usersprofile',
            name='origin',
            field=models.CharField(choices=[('AR', 'Argentina'), ('BR', 'Brazil'), ('BZ', 'Belize'), ('CA', 'Canada'), ('CL', 'Chile'), ('CO', 'Colombia'), ('CR', 'Costa Rica'), ('GT', 'Guatemala'), ('HN', 'Honduras'), ('MX', 'Mexico'), ('NI', 'Nicaragua'), ('PA', 'Panama'), ('SV', 'El Salvador'), ('US', 'United States')], max_length=50, null=True, verbose_name='Origin'),
        ),
    ]
