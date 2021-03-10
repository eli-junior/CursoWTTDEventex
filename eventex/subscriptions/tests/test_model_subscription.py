from eventex.subscriptions.models import Subscription
from django.test import TestCase
from datetime import datetime


class SubscriptionModelTest(TestCase):
    def setUp(self) -> None:
        self.obj = Subscription(
            name='Eli Junior',
            cpf='12345678901',
            email='elijr.net@gmail.com',
            phone='61982110800'
        )
        self.obj.save()

    def test_create(self):
        """Subscription create almost an element on database."""
        self.assertTrue(Subscription.objects.exists())

    def test_created_at(self):
        """Subscription must have an auto created_at attr."""
        self.assertIsInstance(self.obj.created_at, datetime)
