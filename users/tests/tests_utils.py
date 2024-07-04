from django.test import TestCase
from users.utils import validate_password, is_email


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

