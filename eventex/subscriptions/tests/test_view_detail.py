from django.test import TestCase

from eventex.subscriptions.models import Subscription


class SubscriptionDetailGet(TestCase):
    def setUp(self) -> None:
        self.dados = {'name': 'Eli Júnior',
                      'cpf': '00000000191',
                      'email': 'elijr.net@gmail.com',
                      'phone': '61982110800',
                      }
        self.obj = Subscription.objects.create(**self.dados)
        self.resp = self.client.get('/inscricao/%d/' % self.obj.pk)


    def test_get(self):
        """GET /inscrição/ must return code 200"""
        self.assertEqual(200, self.resp.status_code)


    def test_template(self):
        """Must use subscriptions/subscription_detail.html"""
        self.assertTemplateUsed(
            self.resp,
            'subscriptions/subscription_detail.html'
        )

    def test_context(self):
        subscription = self.resp.context['subscription']
        self.assertIsInstance(subscription, Subscription)

    def test_html(self):
        with self.subTest():
            for dado in self.dados.values():
                self.assertContains(self.resp, dado)

class SubscriptionDetailNotFound(TestCase):
    def setUp(self) -> None:
        self.resp = self.client.get('/inscricao/0/')

    def test_not_found(self):
        self.assertEqual(404, self.resp.status_code)
