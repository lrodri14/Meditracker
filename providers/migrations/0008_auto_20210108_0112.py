# Generated by Django 2.2.13 on 2021-01-08 01:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0007_auto_20210106_1610'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='provider',
            options={'verbose_name': 'Provider', 'verbose_name_plural': 'Providers'},
        ),
        migrations.AlterModelOptions(
            name='visitor',
            options={'verbose_name': 'Visitor', 'verbose_name_plural': 'Visitors'},
        ),
    ]
