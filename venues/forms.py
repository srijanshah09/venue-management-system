from django import forms
from .models import *

class VenueCreationForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = [
            "title",
            "contact",
            "bank_account",
        ]