from django.test import TestCase

from users.models import *
from users.utils import *


class ValidatePasswordTestCase(TestCase):
    def test_valid_password(self):
        password = "StrongPassword123"
        self.assertTrue(validate_password(password))

    def test_invalid_short_password(self):
        password = "Short"
        self.assertFalse(validate_password(password))


class IsEmailTestCase(TestCase):
    def test_valid_email(self):
        email = "test@example.com"
        self.assertTrue(is_email(email))

    def test_invalid_email_no_at_symbol(self):
        email = "plainaddress"
        self.assertFalse(is_email(email))

    def test_invalid_email_missing_domain(self):
        email = "username@.com"
        self.assertFalse(is_email(email))

    def test_invalid_email_missing_tld(self):
        email = "username@com"
        self.assertFalse(is_email(email))

    def test_invalid_email_double_dot(self):
        email = "username@domain..com"
        self.assertFalse(is_email(email))


class IsMobileTestCase(TestCase):
    def test_valid_mobile(self):
        mobile = "9876543210"
        self.assertTrue(is_mobile(mobile))


class ValidateDataTestCase(TestCase):

    def test_valid_data(self):
        data = {
            "name": "test",
            "username": "test123",
            "password": "Q!w2e3r4",
            "mobile": "9876543210",
        }
        self.assertTrue(validate_data(data))


class RegisterUserTestCase(TestCase):

    def setUp(self) -> None:
        self.data = {
            "name": "test",
            "username": "test123",
            "password": "Q!w2e3r4",
            "mobile": "9876543210",
        }

    def test_user_saved(self):
        self.assertIsNotNone(register_user(self.data))


class RegisterUserTestCase(TestCase):

    def setUp(self) -> None:
        self.data = {
            "name": "test",
            "username": "test123",
            "password": "Q!w2e3r4",
            "mobile": "9876543210",
        }
        user = register_user(self.data)

    def test_user_token_generation(self):
        self.client.login(
            username=self.data["username"], password=self.data["password"]
        )
        self.assertIn("_auth_user_id", self.client.session)
        self.assertEqual(
            int(self.client.session["_auth_user_id"]),
            User.objects.get(username=self.data["username"]).id,
        )
        user = User.objects.get(username=self.data["username"])
        self.assertIsNotNone(get_tokens_for_user(user))


class GenerateOTPTestCase(TestCase):
    def setUp(self) -> None:
        self.mobile = "9876543210"
    
    def test_generate_otp(self):
        otp = generate_otp(self.mobile)
        self.assertIsNotNone(otp)
        self.assertEqual(len(str(otp)), 4)