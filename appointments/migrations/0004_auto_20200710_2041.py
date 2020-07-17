# Generated by Django 2.2.13 on 2020-07-10 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0003_auto_20200710_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consults',
            name='motive',
            field=models.TextField(help_text='The motive of your assistance to the consult', max_length=100, null=True, verbose_name='motive of the consult'),
        ),
    ]
