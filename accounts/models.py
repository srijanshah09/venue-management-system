from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class CustomUser(models.Model):
    """Model definition for CustomUser."""

    # TODO: Define fields here
    name = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(_('email address'),blank=True, null=True, unique=True)
    mobile = models.CharField(max_length=15,unique=True)
    profile_image = models.ImageField(upload_to="profile/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta definition for CustomUser."""

        verbose_name = 'CustomUser'
        verbose_name_plural = 'CustomUsers'

    def __str__(self):
        """Unicode representation of CustomUser."""
        return f"{self.username}"
