# Generated by Django 2.2.13 on 2020-09-17 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0034_auto_20200917_0319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='gender',
            field=models.CharField(choices=[('F', 'Femenine'), ('M', 'Masculine'), ('O', 'Other')], help_text='Gender', max_length=20, null=True, verbose_name="Patient's Gender"),
        ),
    ]
