from celery import shared_task
from .models import Consults
from django.contrib.auth import get_user_model
from django.utils import timezone


@shared_task()
def change_status():
    consults = Consults.objects.all()
    for c in consults:
        if c.status == 'OPEN' and c.datetime.date < timezone.localtime(timezone.now()).date():
            c.status = 'CLOSED'
            c.save()
        else:
            pass