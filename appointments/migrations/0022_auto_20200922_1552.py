# Generated by Django 2.2.13 on 2020-09-22 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0021_auto_20200922_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consults',
            name='charge',
            field=models.FloatField(help_text='Charge Amount', null=True, verbose_name='charge'),
        ),
    ]
