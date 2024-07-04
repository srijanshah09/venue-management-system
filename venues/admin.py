from django.contrib import admin

from .models import State, City, Venue, BankAccount, Address, Availability

# Register your models here.
admin.site.register(State)
admin.site.register(City)
admin.site.register(Address)
admin.site.register(BankAccount)
admin.site.register(Availability)
admin.site.register(Venue)
