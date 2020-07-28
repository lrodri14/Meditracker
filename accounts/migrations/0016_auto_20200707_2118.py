# Generated by Django 2.2.13 on 2020-07-07 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20200707_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersprofile',
            name='location',
            field=models.CharField(choices=[('HND', 'Honduras')], help_text='Provide your location', max_length=100, null=True, verbose_name='location'),
        ),
    ]