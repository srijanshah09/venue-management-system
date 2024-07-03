from django.forms import ValidationError
from django.test import TestCase
from users.models import User
# Create your tests here.


class UserModelTestCase(TestCase):
    def test_custom_user_model_exists(self):
        """    
        ## test_custom_user_model_exists
        Checks if there are any instances of the `User` model in the database.

        ### Returns
        - None

        ### Raises
        - AssertionError: If the count of instances of the `User` model is not equal to 0.
        """
        custom_user = User.objects.all()
        self.assertEqual(custom_user.count(), 0)

    def test_string_rep_of_objects(self):
        """
        ## test_string_rep_of_objects

        Tests the string representation of objects created using the `User` model.

        ### Returns
        - None

        ### Raises
        - AssertionError: If the string representation of the user object does not match the user's name.

        """
        user = User.objects.create(
            username = "admin",
            password = "Q!w2e3r4",
            name="admin"
        )
        self.assertEqual(str(user), user.name)
        
    def test_user_creation(self):
        """
        ## test_user_creation
        
        Tests the creation of a new user instance with specified attributes.
        
        ### Returns
        - None
        
        ### Raises
        - AssertionError: If the attributes of the created user instance do not match the expected values.

        """
        user = User.objects.create(username='testuser', name='Test User', email='test@example.com', mobile='1234567890')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.name, 'Test User')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.mobile, '1234567890')

    def test_user_creation_invalid_email(self):
        """
        ## test_user_creation_invalid_email

        Tests the validation of user creation with an invalid email address.
        
        ### Returns
        - None
        
        ### Raises
        - ValidationError: If the user creation with an invalid email address does not raise a validation error.

        """
        with self.assertRaises(ValidationError):
            user = User(username='testuser', name='Test User', email='invalidemail', mobile='1234567890')
            user.save()
            user.full_clean()

    def test_user_creation_duplicate_mobile(self):
        """
        ## test_user_creation_duplicate_mobile

        Tests the validation of user creation with an duplicate mobile number.
        
        ### Returns
        - None
        
        ### Raises
        - ValidationError: If the user creation with an duplicate mobile number, does not raise a validation error.
        """
        User.objects.create(username='existing_user', name='Existing User', email='existing@example.com', mobile='1234567890')
        with self.assertRaises(ValidationError):
            user = User(username='testuser', name='Test User', email='test@example.com', mobile='1234567890')
            user.full_clean()

