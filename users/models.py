from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import *

# Create your models here.

ROLE_CHOICES = (
    ('partner','partner'),
    ('customer', 'customer'),
    ('admin','admin'),
)

class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class User(CustomUser):
    role = models.CharField(choices=ROLE_CHOICES, max_length=50, default='customer')

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return f"{self.username}"
    


class Otp(Base):
    email = models.EmailField(blank=True, null=True,)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    otp = models.PositiveIntegerField(default=1111)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self) -> str:
        return f"{self.mobile}"