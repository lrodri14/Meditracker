"""
    DOCSTRING:
    This models.py file contains all the models used to create instances of CIE-10-Groups, Drugs, Medical exams and
    consults itself, this .py file is composed of four models.
"""

# Imports
from django.db import models
from patients.models import Patient
from django.contrib.auth import get_user_model
# Getting the user model
user = get_user_model()

# Create your models here.


class Cie10Group(models.Model):
    """
        DOCSTRING:
        The Cie10Group modal is used to create CIE-10 code instances, it's composed of only one attribute, the code itself,
        we also created it's own __str__ dunder method representation, this mode overwrote it's save method, we added
        some functionality to capitalize the code once it reaches the database. It inherits from the models.Model class.
    """

    code = models.CharField('code', max_length=50, blank=False, null=True, help_text='CIE-10 Code')

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        self.code = self.code.capitalize()
        super(Cie10Group, self).save(*args, **kwargs)


class Drug(models.Model):
    """
        DOCSTRING:
        The Drug modal inherits from the models.Model class, it is used to create Drug instances as needed, this model
        defines a tuple under the variable CATEGORY_CHOICES, this choices are used to specify to what branch does this
        drug belongs, we added some functionality through the META CLASS indicating that the 'name' and 'created_by'
        are unique inside our instances, we also set our own __str__ dunder method and we overwrote the save method to
        capitalize the name of the drug every time it reaches the database.
    """

    CATEGORY_CHOICES = (
        ('AP', 'Antipyretics'),
        ('AG', 'Analgesics'),
        ('AM', 'Antimalarial'),
        ('AB', 'Antibiotics'),
        ('AS', 'Antiseptics'),
        ('MS', 'Mood Stabilizers'),
        ('HR', 'Hormone Replacement'),
        ('OC', 'Oral Contraceptives'),
        ('S', 'Stimulants'),
        ('T', 'Tranquilizers'),
        ('ST', 'Statins'),

    )
    name = models.CharField('drug', max_length=200, blank=False, null=True, help_text='drugs name')
    category = models.CharField('category', max_length=50, blank=False, null=True, help_text='Category', choices=CATEGORY_CHOICES)
    created_by = models.ForeignKey(user, on_delete=models.CASCADE, blank=True, null=True, help_text='Drug created by',
                                   related_name='created_by', verbose_name='Created By')

    class Meta:
        unique_together = ['name', 'created_by']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        super(Drug, self).save(*args, **kwargs)


class Consult(models.Model):
    """
        DOCSTRING:
        The Consult class inherits from the models.Model class, it is used to create consults, and update consults
        once they were scheduled, *NOTE: once consults have been scheduled, filled with diagnose related data and saved
        can not be updated, this to prevent any possible misinformation*, we declared a tuple of choices which will
        establish in which state does the consult remains, the 'medical_status' attribute sets the status of the consult,
        to True if it was attended, and False if it was not, also the 'lock' attribute, is used to keep the consult active
        to further changes, until the lock attribute is set to True, then the consult will be closed and will never be
        able to be open again. We added some functionality, defining a META class, and set the unique_together attribute
        to 'patient' and 'datetime' attributes, fianlly we created our own __str__ dunder method and rewrote the save
        method, capitalizing the 'motive' and 'suffering' attributes once they reach the database.
    """

    STATUS_CHOICES = (
        ('OPEN', 'Open'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('CLOSED', 'Closed'),
    )

    # Consult creator
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=False, null=True, verbose_name='patient',
                                help_text='Patient assisting this consult', related_name='patient')
    datetime = models.DateTimeField('Date of the consult', blank=False, null=True, help_text='Date the consult will be done')
    motive = models.TextField('motive of the consult', blank=False, null=True,
                              help_text='The motive of your assistance to the consult')
    suffering = models.TextField('suffering', blank=False, null=True,
                                 help_text='What is the patient suffering?')
    charge = models.DecimalField('charge', blank=False, null=True, max_digits=10, decimal_places=2, help_text='Charge Amount')
    created_by = models.ForeignKey(user, on_delete=models.CASCADE, blank=True, null=True,
                                   help_text='Creator of the consult', verbose_name='created by', related_name='author')
    # Consult Content
    # Vital Signs
    blood_pressure = models.FloatField('blood pressure', blank=True, null=True, help_text='blood pressure')
    temperature = models.FloatField('temperature', blank=True, null=True, help_text='body temperature')
    weight = models.FloatField('weight', blank=True, null=True, help_text='weight')
    size = models.FloatField('size', blank=True, null=True, help_text='size')
    # Organ System
    digestive_system = models.TextField('digestive system', blank=True, null=True, help_text='digestive system analysis')
    endocrine_system = models.TextField('endocrine system', blank=True, null=True, help_text='endocrine system analysis')
    renal_system = models.TextField('renal system', blank=True, null=True, help_text='renal system analysis')
    lymphatic_system = models.TextField('lymphatic system', blank=True, null=True, help_text='lymphatic system analysis')
    respiratory_system = models.TextField('respiratory system', blank=True, null=True, help_text='respiratory system analysis')
    # Physical Exploration
    head_exploration = models.TextField('head exploration', blank=True, null=True, help_text='head exploration analysis')
    thorax_exploration = models.TextField('thorax exploration', blank=True, null=True, help_text='thorax exploration analysis')
    # Diagnose
    cie_10_group = models.OneToOneField(Cie10Group, on_delete=models.CASCADE, blank=True, null=True, help_text='CIE-10 group for the diagnose',
                                        verbose_name='CIE-10 Group', related_name='ciegroup')
    cie_10_detail = models.TextField('CIE-10 Detail', blank=True, null=True, help_text='CIE-10 diagnose details')
    diagnose = models.TextField('diagnose', blank=True, null=True, help_text='Diagnose')
    procedure = models.TextField('procedure', blank=True, null=True, help_text='Procedure')
    analysis = models.TextField('analysis', blank=True, null=True, help_text='Analysis')
    notes = models.TextField('notes', blank=True, null=True, help_text='Notes')
    # Treatmenet
    drugs = models.ManyToManyField(Drug, blank=True, help_text='Drugs recommended', verbose_name='Drugs', related_name='drugs')
    indications = models.TextField('indications', blank=True, null=True, help_text='Indications')
    actions = models.TextField('actions', blank=True, null=True, help_text='actions')
    prescription = models.FileField('prescription', blank=True, null=True, help_text="Current consult's prescription", upload_to='appointments/prescriptions')
    # Status
    medical_status = models.BooleanField('medical_status', blank=True, null=True, help_text='Handles the medical consult status', default=False)
    status = models.CharField('status', max_length=10, blank=True, null=True, help_text='Handles the consult status', default=STATUS_CHOICES[0][0], choices=STATUS_CHOICES)
    lock = models.BooleanField('lock', default=True, blank=False, null=True, help_text='Consult lock status')

    class Meta:
        unique_together = ['created_by', 'datetime']

    def __str__(self):
        return str(self.patient) + "'s consult for " + str(self.datetime)

    def save(self, *args, **kwargs):
        self.suffering = self.suffering.capitalize()
        self.motive = self.motive.capitalize()
        super(Consult, self).save(*args, **kwargs)


class MedicalExam(models.Model):

    """
        DOCSTRING:
        The MedicalExam model inherits from the models.Model class and is used to create exams instances, we defined a
        tuple of choices under the name of EXAMS_CHOICES, used to indicate what type of exam we are creating, we also
        created our own dunder __str__ dunder method.
    """

    EXAMS_CHOICES = (
        ('T', 'Test'),
    )
    consult = models.ForeignKey(Consult, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Medical Exams', help_text='Medical Exams', related_name='exams')
    date = models.DateField('date', blank=True, null=True, help_text='Date the exams were presented')
    type = models.CharField('type of exams', max_length=100, blank=False, null=True, help_text='Type of exams', choices=EXAMS_CHOICES)
    image = models.ImageField('exam', blank=True, null=True, help_text='Exam IMG', upload_to='appointments/exams')

    def __str__(self):
        return self.type + ' ' + str(self.date)
