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
