from django.db import models
from django.apps import apps
from django.utils import timezone
from patients.models import Patient
from django.contrib.auth import get_user_model
user = get_user_model()


# Create your models here.


class Cie10Group(models.Model):
    code = models.CharField('code', max_length=50, blank=False, null=True, help_text='CIE-10 Code')

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        self.code = self.code.capitalize()
        super(Cie10Group, self).save(*args, **kwargs)


class Consults(models.Model):

    STATUS_CHOICES = (
        ('OPEN', 'Open'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('CLOSED', 'Closed'),
    )

    # Consult creator
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=False, null=True, verbose_name='patient',
                                help_text='Patient assisting, this consult', related_name='patient')
    datetime = models.DateTimeField('Date of the consult', blank=False, null=True, help_text='Date the consult will be done')
    motive = models.TextField('motive of the consult', blank=False, null=True,
                              help_text='The motive of your assistance to the consult')
    suffering = models.TextField('suffering', blank=False, null=True,
                                 help_text='What is the patient suffering?')
    created_by = models.ForeignKey(user, on_delete=models.CASCADE, blank=True, null=True,
                                   help_text='Creator of the consult', verbose_name='created by', related_name='author')
    # Consult Content
    # Vital Signs
    blood_pressure = models.FloatField('blood pressure', blank=True, null=True, help_text='blood pressure')
    temperature = models.FloatField('temperature', blank=True, null=True, help_text='body temperature')
    weight = models.FloatField('weight', blank=True, null=True, help_text='weight')
    size = models.FloatField('size', blank=True, null=True, help_text='size')
    # Exams
    medical_exams = models.FileField('medical exams', blank=True, null=True, help_text='Attach exams if availalble',
                                     upload_to='appointmens/exams')
    # Organ System
    digestive_system = models.TextField('digestive system', blank=True, null=True, help_text='digestive system analysis')
    endocrine_system = models.TextField('endocrine system', blank=True, null=True, help_text='endocrine system analysis')
    renal_system = models.TextField('renal system', blank=True, null=True, help_text='renal system analysis')
    lymphatic_system = models.TextField('lymphatic system', blank=True, null=True, help_text='lymphatic system analysis')
    respiratory_system = models.TextField('respiratory system', blank=True, null=True, help_text='respiratory system analysis')
    # Physical Exploration
    head_exploration = models.TextField('head exploration', blank=True, null=True, help_text='head exploration analysis')
    thorax_exploration = models.TextField('thorax exploration', blank=True, null=True, help_text='thorax exploration analysis')
    # Diagnose and treatment
    cie_10_group = models.OneToOneField(Cie10Group, on_delete=models.CASCADE, blank=True, null=True, help_text='CIE-10 group for the diagnose',
                                        verbose_name='CIE-10 Group', related_name='ciegroup')
    cie_10_detail = models.TextField('CIE-10 Detail', blank=True, null=True, help_text='CIE-10 diagnose details')
    diagnose = models.TextField('diagnose', blank=True, null=True, help_text='Diagnose')
    procedure = models.TextField('procedure', blank=True, null=True, help_text='Procedure')
    analysis = models.TextField('analysis', blank=True, null=True, help_text='Analysis')
    notes = models.TextField('notes', blank=True, null=True, help_text='Notes')
    # Treatmenet
    medicine = models.TextField('medicine', blank=True, null=True, help_text='Medicine')
    actions = models.TextField('actions', blank=True, null=True, help_text='actions')
    # Status
    medical_status = models.BooleanField('medical_status', blank=True, null=True, help_text='Handles the medical consult status', default=False)
    status = models.CharField('status', max_length=10, blank=True, null=True, help_text='Handles the consult status', default=STATUS_CHOICES[0][0], choices=STATUS_CHOICES)

    def __str__(self):
        return str(self.patient) + "'s consult for " + str(self.datetime)

    def save(self, *args, **kwargs):
        self.suffering = self.suffering.capitalize()
        self.motive = self.motive.capitalize()
        super(Consults, self).save(*args, **kwargs)

    class Meta:
        unique_together = ['patient', 'datetime']


class Drugs(models.Model):
    name = models.CharField('drugs', max_length=200, blank=True, null=True, unique=True, help_text='drugs name')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        super(self, Drugs).save(*args, **kwargs)