from django.test import TestCase
from users.models import *
from http import HTTPStatus


class HomePageTestCase(TestCase):
    def setUp(self) -> None:
        user1 = User.objects.create(
            username="testuser1",
            name="Test User",
            email="test1@example.com",
            mobile="1234567890",
        )
        user2 = User.objects.create(
            username="testuser2",
            name="Test User",
            email="test2@example.com",
            mobile="1234567891",
        )

    def test_homepage_returns_correct_response(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "users/index.html")
        self.assertEqual(response.status_code, HTTPStatus.OK)
    
    def test_homepage_returns_list_users(self):
        response = self.client.get("/")
        self.assertContains(response, "testuser1")
        self.assertContains(response, "testuser2")

class DetailsPageTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
                username="testuser3",
                name="Test User",
                email="test3@example.com",
                mobile="1234567893",
            )
    
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
