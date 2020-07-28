from celery import shared_task
from .models import Consults
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
