from django.test import TestCase
from django.contrib.auth import get_user_model
from model_bakery import baker
from venues.models import *

User = get_user_model()


class VenueOwnerTest(TestCase):
    def setUp(self) -> None:
        self.user = baker.make(User)
        self.bank = baker.make(BankAccount)
        self.venue = Venue.objects.create(
            title="Test Venue",
            owner=self.user,
            bank_account=self.bank,
        )

    def test_user_is_instance_of_user_model(self):
        self.assertTrue(isinstance(self.user, User))

    def venue_belongs_to_user(self):
        self.assertTrue(hasattr(self.venue, self.user))
        self.assertEqual(self.venue.owner, self.user)
