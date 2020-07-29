from __future__ import absolute_import
from celery import shared_task
from .models import Consults, Drugs
from django.utils import timezone


@shared_task
def change_status():
    consults = Consults.objects.all()
    for c in consults:
        if c.status == 'OPEN' and c.datetime.date() < timezone.localtime().date():
            c.status = 'CLOSED'
            c.save()
        else:
            continue


@shared_task
def save_new_drug(drugs):
    if drugs:
        for drug in drugs:
            new_drug = Drugs.objects.create(name=drug)
            new_drug.save()
        else:
            pass
