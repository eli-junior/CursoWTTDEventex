from django.conf import settings
from django.core import mail
from django.test import TestCase

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription
from django.shortcuts import resolve_url as r

# Force Send Email for Tests
settings.SEND_EMAIL = True


class SubscribeNewGet(TestCase):
    def setUp(self) -> None:
        self.resp = self.client.get(r('subscriptions:new'))

    def test_get(self):
        """GET /inscrição/ must return code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Must use subscriptions/subscription_form.html"""
        self.assertTemplateUsed(
            self.resp, 'subscriptions/subscription_form.html')

    def test_html(self):
        """HTML must contain input tags"""
        tags = (('<form', 1),
                ('<input', 6),
                ('type="text"', 3),
                ('type="email"', 1),
                ('type="submit"', 1))

        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)

    def test_csrf(self):
        """HTML must return csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscription form"""
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)


class SubscriptionNewPostValid(TestCase):
    def setUp(self) -> None:
        self.dados = {'name': 'Eli Júnior',
                      'cpf': '00000000191',
                      'email': 'elijr.net@gmail.com',
                      'phone': '61982110800',
                      }
        self.resp = self.client.post(r('subscriptions:new'), self.dados)
        self.email = mail.outbox[0]

    def test_post(self):
        """Valid POST should redirect to /inscricao/id/"""
        self.assertRedirects(self.resp, r('subscriptions:detail', self.resp.url[11:-1]))

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_save_subscription(self):
        self.assertTrue(Subscription.objects.exists())


class SubscriptionNewPostInvalid(TestCase):
    def setUp(self) -> None:
        self.resp = self.client.post(r('subscriptions:new'), {})
        self.form = self.resp.context['form']

    def test_post(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        self.assertIsInstance(self.form, SubscriptionForm)

    def test_form_has_errors(self):
        self.assertTrue(self.form.errors)

    def test_save_subscription(self):
        self.assertFalse(Subscription.objects.exists())
