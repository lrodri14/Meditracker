# Generated by Django 2.2.13 on 2021-01-12 02:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0025_auto_20210111_1633'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_user', models.ForeignKey(blank=True, help_text='User sending the request', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Request Sender')),
                ('to_user', models.ForeignKey(blank=True, help_text='User to send the request', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='request', to=settings.AUTH_USER_MODEL, verbose_name='Request Receive')),
            ],
            options={
                'verbose_name': 'Contact Request',
                'verbose_name_plural': 'Contact Requests',
            },
        ),
    ]
