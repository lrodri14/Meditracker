# Generated by Django 2.2.13 on 2021-01-12 22:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0026_contactrequest'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='contactrequest',
            unique_together={('from_user', 'to_user')},
        ),
    ]
