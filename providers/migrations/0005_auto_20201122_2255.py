# Generated by Django 2.2.13 on 2020-11-22 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '0004_auto_20201117_0350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitor',
            name='last_name',
            field=models.CharField(blank=True, help_text="Visitor's Last Name", max_length=100, null=True, verbose_name="Visitor's Last Name"),
        ),
    ]
