# Generated by Django 2.2.13 on 2020-06-23 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200621_1459'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersprofile',
            name='address',
            field=models.CharField(help_text='Provide your address', max_length=200, null=True, verbose_name='address'),
        ),
    ]
