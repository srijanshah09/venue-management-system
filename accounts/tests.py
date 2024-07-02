from django.test import TestCase
from .models import *
# Create your tests here.

class CustomUserModelTest(TestCase):
    def test_custom_user_model_exists(self):
        custom_user = CustomUser.objects.all()

        self.assertEqual(custom_user.count(), 0)