from http import HTTPStatus

from django.test import TestCase
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from model_bakery import baker

from users.models import *
from users.forms import *


class DetailsPageTest(TestCase):
    def setUp(self) -> None:
        self.user = baker.make(User)

    def test_detail_page_correct_response(self):
        response = self.client.get(self.user.get_absolute_url())
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/user-details.html")

    def test_detail_page_correct_information(self):
        response = self.client.get(self.user.get_absolute_url())
        self.assertContains(response, self.user.username)
        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.mobile)
        self.assertContains(response, self.user.email)


class UserCreationPageTest(TestCase):
    def setUp(self) -> None:
        self.form_class = UserRegistrationForm

    def test_creation_page_exists(self):
        response = self.client.get(reverse("users:signup_page"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed("users/signup.html")
        self.assertContains(response, "Create your Account")

    def test_signup_form_works_correctly(self):
        self.assertTrue(issubclass(UserRegistrationForm, UserCreationForm))
        self.assertTrue("email" in self.form_class.Meta.fields)
        self.assertTrue("username" in self.form_class.Meta.fields)
        self.assertTrue("password1" in self.form_class.Meta.fields)
        self.assertTrue("password2" in self.form_class.Meta.fields)
        sample_data = {
            "email": "srijanshah09@gmail.com",
            "username": "admin",
            "mobile": "9582218879",
            "password1": "Q!w2e3r4",
            "password2": "Q!w2e3r4",
        }
        form = self.form_class(sample_data)
        self.assertTrue(form.is_valid())

    def test_signup_form_creates_user_in_db(self):
        user = {
            "email": "srijanshah09@gmail.com",
            "username": "admin",
            "mobile": "9582218879",
            "password1": "Q!w2e3r4",
            "password2": "Q!w2e3r4",
        }
        form = self.form_class(user)
        if form.is_valid():
            form.save()
        self.assertEqual(User.objects.count(), 1)


class LoginTest(TestCase):
    def setUp(self) -> None:
        self.username = "test123"
        self.email = "test@gmail.com"
        self.mobile = "9582218879"
        self.password = "Q!w2e3r4"
        User.objects.create_user(
            username=self.username,
            email=self.email,
            mobile=self.mobile,
            password=self.password,
        )

    def test_login_page_exists(self):
        response = self.client.get(reverse("users:login_page"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/login.html")

    def test_login_page_has_login_form(self):
        response = self.client.get(reverse("users:login_page"))
        form = response.context.get("form")

        self.assertIsInstance(form, AuthenticationForm)

    def test_login_page_logs_user_in(self):
        user_data = {
            "username": self.username,
            "password": self.password,
        }
        response = self.client.post(reverse("users:login_page"), user_data)
        self.assertRedirects(response, reverse("venues:dashboard_overview"))


class LogoutTest(TestCase):
    def setUp(self) -> None:
        self.username = "test123"
        self.email = "test@gmail.com"
        self.mobile = "9582218879"
        self.password = "Q!w2e3r4"
        User.objects.create_user(
            username=self.username,
            email=self.email,
            mobile=self.mobile,
            password=self.password,
        )

    def test_logout_view_logs_out_user(self):
        self.client.login(username=self.username, password=self.password)
        self.assertTrue("_auth_user_id" in self.client.session)
        response = self.client.get(reverse("users:logout"))
        self.assertFalse("_auth_user_id" in self.client.session)
