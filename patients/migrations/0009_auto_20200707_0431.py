# Generated by Django 2.2.13 on 2020-07-07 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0008_auto_20200705_0138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='age',
            field=models.DateField(null=True, verbose_name='patients age'),
        ),
    ]
