from django.db import models
from users.models import User
# Create your models here.

ACCOUNT_TYPE_CHOICES = [
    ('saving', 'Saving'),
    ('current', 'Current Account'),
    ('credit', 'Cash Credit'),
    ('loan', 'Loan Account'),
]
DAY_CHOICES = [
    ('sunday', 'sunday'),
    ('monday', 'monday'),
    ('tuesday', 'tuesday'),
    ('wednesday', 'wednesday'),
    ('thursday', 'thursday'),
    ('friday', 'friday'),
    ('saturday', 'saturday'),
]

class State(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey('State', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    
class Address(models.Model):
    first_line = models.TextField(blank=True, default="")
    city = models.ForeignKey('City', on_delete=models.CASCADE)
    pincode = models.CharField(max_length=10, default="", blank=True)

class BankAccount(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    account_holder_name = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)
    ifsc_code = models.CharField(max_length=20)
    account_number = models.CharField(max_length=50)
    account_type = models.CharField(choices=ACCOUNT_TYPE_CHOICES,max_length=100,default='saving')
    nick_name= models.CharField(max_length=200)

class Venue(models.Model):
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    map_link = models.URLField(max_length=500, null=True, blank=True)
    address = models.ForeignKey('Address', null=True, blank=True, on_delete=models.SET_NULL)
    contact = models.CharField(max_length=20, null=True, blank=True)
    bank_account = models.ForeignKey('BankAccount', on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=True)

class Availability(models.Model):
    venue = models.ForeignKey('Venue', on_delete=models.CASCADE)
    day = models.CharField(choices=DAY_CHOICES, max_length=20, default="sunday")
    is_open = models.BooleanField(default=True)

    class Meta:
        unique_together = ['venue', 'day']