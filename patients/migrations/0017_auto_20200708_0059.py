# Generated by Django 2.2.13 on 2020-07-08 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0016_auto_20200708_0057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insurancecarrier',
            name='company',
            field=models.CharField(help_text='Insurance Carrier', max_length=100, verbose_name='company'),
        ),
    ]
