from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.http.request import HttpRequest
from django.contrib.auth import get_user_model

from model_bakery import baker

from venues.forms import VenueCreationForm
from venues.models import *
from users.models import User

class VenueCreationTest(TestCase):

    def setUp(self) -> None:
        self.url= reverse('create_venue')
        self.template_name = "venues/create_venue.html"
        self.form_class = VenueCreationForm
        self.title = "Football ground"
        self.contact = "9582218879"
        self.bank_account = baker.make(BankAccount)
        self.user = User.objects.create_user(
            username="admin",
            password="password",
            name="admin",
            mobile="9582218879",
            email="srijanshah09@gmail.com"
        )
        

    def test_venue_creation_page_exists(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, self.template_name)
        form = response.context.get('form', None)
        self.assertIsInstance(form, self.form_class)

    def test_post_creation_form(self):
        post_request = HttpRequest()
        post_request.user = baker.make(get_user_model())
        venue_data = {
            "title": self.title,
            "contact": self.contact,
            "bank_account": self.bank_account,
        }
        post_request.POST = venue_data
        
        form = self.form_class(post_request.POST)
        self.assertTrue(form.is_valid())
        venue_object = form.save(commit=False)
        self.assertIsInstance(venue_object, Venue)

        venue_object.owner = post_request.user
        venue_object.save()
        self.assertEqual(Venue.objects.count(),1)

    def test_post_creation_requires_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, expected_url="/login-page/?next=/create-venue/")
        self.client.login(username='admin', password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
