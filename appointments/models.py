from django.db import models
from django.apps import apps
from patients.models import Patient
from django.contrib.auth import get_user_model
user = get_user_model()


# Create your models here.


class Consults(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=False, null=True, verbose_name='patient',
                                help_text='Patient assisting, this consult', related_name='patient')
    date = models.DateField('Date of the consult', blank=False, null=True, help_text='Date the consult will be done')
    time = models.TimeField('Time of the consult', blank=False, null=True, help_text='Time the consult will be done')
    motive = models.CharField('motive of the consult', max_length=100, blank=False, null=True,
                              help_text='The motive of your assistance to the consult', default='Protocol')
    suffering = models.CharField('suffering', max_length=250, blank=False, null=True,
                                 help_text='What is the patient suffering?')
    created_by = models.ForeignKey(user, on_delete=models.CASCADE, blank=False, null=True,
                                   help_text='Creator of the consult', verbose_name='created by', related_name='author')

    class Meta:
        unique_together = ['patient', 'date', 'time']

    def __str__(self):
        return str(self.patient) + "'s consult for " + str(self.date)

    def save(self, *args, **kwargs):
        self.motive = self.motive.capitalize()
        self.suffering = self.suffering.capitalize()
        super(Consults, self).save(*args, **kwargs)
