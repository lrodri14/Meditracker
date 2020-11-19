from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.


class Providers(models.Model):

    PROVIDERS_TYPE_CHOICES = (
        ('LP', 'Laboratory'),
        ('MP', 'Medical Provider')
    )

    company = models.CharField('Company', max_length=100, blank=False, null=True, help_text="Provider's Brand")
    address = models.CharField('Address', max_length=250, blank=False, null=True, help_text="Company's Address")
    email = models.EmailField('Email', blank=False, null=True, help_text="Company's Email")
    contact = models.CharField('Phone Number', max_length=100, blank=False, null=True, help_text='Providers Contact')
    provider_type = models.CharField('Type', max_length=100, blank=True, null=True, help_text="Provider's Type", choices=PROVIDERS_TYPE_CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, help_text='Created By')

    class Meta:
        unique_together = ['company', 'created_by']
        
    def save(self, *args, **kwargs):
        self.company = self.company.title()
        self.address = self.address.capitalize()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.company


class Visitor(models.Model):

    name = models.CharField("Visitor's Name", max_length=100, blank=True, null=True, help_text="Visitor's First Name")
    last_name = models.CharField("Visitor's Last Name", max_length=100, blank=True, null=True, help_text="Visitor's Last Name")
    contact = models.CharField('Phone Number', max_length=100, blank=False, null=True, help_text="Visitor's Contact")
    email = models.EmailField('Email', blank=False, null=True, help_text="Visitor's Email")
    company = models.ForeignKey(Providers, on_delete=models.CASCADE, blank=False, null=True, help_text='Providers Brand')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, help_text='Created By')

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        self.last_name = self.last_name.title()
        super().save(*args, **kwargs)


