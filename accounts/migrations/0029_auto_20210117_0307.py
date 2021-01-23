# Generated by Django 2.2.13 on 2021-01-17 03:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0028_chat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='destination',
        ),
        migrations.RemoveField(
            model_name='chat',
            name='origin',
        ),
        migrations.AddField(
            model_name='chat',
            name='participants',
            field=models.ManyToManyField(blank=True, help_text='Chat Participants', related_name='participants', to=settings.AUTH_USER_MODEL, verbose_name='Participants'),
        ),
    ]
