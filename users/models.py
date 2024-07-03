from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    name = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(_("email address"), blank=True, null=True, unique=True)
    mobile = models.CharField(max_length=15, unique=True)
    profile_image = models.ImageField(upload_to="profile/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return self.username


class Otp(Base):
    email = models.EmailField(
        blank=True,
        null=True,
    )
    mobile = models.CharField(max_length=15, null=True, blank=True)
    otp = models.PositiveIntegerField(default=1111)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self) -> str:
        return f"{self.mobile}"
