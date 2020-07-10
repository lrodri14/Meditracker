# Generated by Django 2.2.13 on 2020-07-09 20:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0021_auto_20200709_2018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allergies',
            name='created_by',
            field=models.ForeignKey(help_text='User by who this allergy was created', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
