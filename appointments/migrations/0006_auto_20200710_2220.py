# Generated by Django 2.2.13 on 2020-07-10 22:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0005_auto_20200710_2052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consults',
            name='created_by',
            field=models.ForeignKey(blank=True, help_text='Creator of the consult', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL, verbose_name='created by'),
        ),
    ]
