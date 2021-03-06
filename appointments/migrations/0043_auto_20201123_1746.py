# Generated by Django 2.2.13 on 2020-11-23 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0042_auto_20201123_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consults',
            name='attended_at',
            field=models.DateTimeField(blank=True, default=None, help_text='Time the consult was attended', null=True, verbose_name='attended_at'),
        ),
        migrations.AlterField(
            model_name='consults',
            name='finished_at',
            field=models.DateTimeField(blank=True, default=None, help_text='Time the consult was finished', null=True, verbose_name='finished_at'),
        ),
    ]
