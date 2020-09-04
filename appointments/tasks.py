from __future__ import absolute_import
from celery import shared_task
from .models import Consults, Drugs
from django.utils import timezone
from django.contrib.auth import get_user_model


# @shared_task
# def change_status():
#     consults = Consults.objects.all()
#     for c in consults:
#         if c.status == 'OPEN' and (c.datetime.astimezone(tzone).date() < date):
#             c.status = 'CLOSED'
#             c.save()
#         else:
#             continue

@shared_task
def save_new_drug(drugs, user_id):
    user = get_user_model().objects.get(id=user_id)
    if drugs:
        for drug in drugs:
            new_drug = Drugs.objects.create(name=drug, created_by=user)
            new_drug.save()
        else:
            pass
