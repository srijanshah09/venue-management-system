from django.forms import ValidationError
from django.test import TestCase
from .models import User
# Create your tests here.


class UserModelTestCase(TestCase):
    def test_custom_user_model_exists(self):
        custom_user = User.objects.all()

        self.assertEqual(custom_user.count(), 0)

    def test_string_rep_of_objects(self):
        user = User.objects.create(
            username = "admin",
            password = "Q!w2e3r4",
            name="admin"
        )
        self.assertEqual(str(user), user.name)
        
    def test_user_creation(self):
        user = User.objects.create(username='testuser', name='Test User', email='test@example.com', mobile='1234567890')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.name, 'Test User')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.mobile, '1234567890')

    def test_user_creation_invalid_email(self):
        with self.assertRaises(ValidationError):
            user = User(username='testuser', name='Test User', email='invalidemail', mobile='1234567890')
            user.full_clean()

    def test_user_creation_duplicate_mobile(self):
        User.objects.create(username='existing_user', name='Existing User', email='existing@example.com', mobile='1234567890')
        with self.assertRaises(ValidationError):
            user = User(username='testuser', name='Test User', email='test@example.com', mobile='1234567890')
            user.full_clean()
