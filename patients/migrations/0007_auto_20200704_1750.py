# Generated by Django 2.2.13 on 2020-07-04 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0006_auto_20200704_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='age',
            field=models.IntegerField(null=True, verbose_name='patients age'),
        ),
    ]
