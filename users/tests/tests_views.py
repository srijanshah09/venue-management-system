from django.test import TestCase
from users.models import *
from http import HTTPStatus
from model_bakery import baker


class HomePageTestCase(TestCase):
    def setUp(self) -> None:
        self.user1 = baker.make(User)
        self.user2 = baker.make(User)

    def test_homepage_returns_correct_response(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "users/index.html")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_homepage_returns_list_users(self):
        response = self.client.get("/")
        self.assertContains(response, self.user1.username)
        self.assertContains(response, self.user2.username)


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
        return super().setUp()
    
    def test_creation_page_exists(self):
        response = self.client.get(reverse("signup_page"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed('users/signup.html')
        self.assertContains(response, "Create your Account")