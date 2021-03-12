from django.core import mail
from django.test import TestCase
from django.shortcuts import resolve_url as r


class SubscribePostValid(TestCase):
    def setUp(self) -> None:
        self.dados = {'name': 'Eli Júnior',
                      'cpf': '00000000191',
                      'email': 'elijr.net@gmail.com',
                      'phone': '61982110800',
                      }
        self.client.post(r('subscriptions:new'), self.dados)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        expect = 'Confirmação de Inscrição'
        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        expect = 'realelijr@gmail.com'
        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        expect = ['realelijr@gmail.com', 'elijr.net@gmail.com']
        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):
        for dado in self.dados.values():
            with self.subTest():
                self.assertIn(dado, self.email.body)
