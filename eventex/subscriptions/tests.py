from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscribeTest(TestCase):
    def setUp(self) -> None:
        self.resp = self.client.get('/inscricao/')

    def test_get(self):
        """GET /inscrição/ must return code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Must use subscriptions/subscription_form.html"""
        self.assertTemplateUsed(
            self.resp, 'subscriptions/subscription_form.html')

    def test_html(self):
        """HTML must contain input tags"""
        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp, '<input', 6)
        self.assertContains(self.resp, 'type="text"', 3)
        self.assertContains(self.resp, 'type="email"')
        self.assertContains(self.resp, 'type="submit"')

    def test_csrf(self):
        """HTML must return csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscription form"""
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fiels(self):
        """Form must have 4 fields"""
        form = self.resp.context['form']
        lista = ['name', 'cpf', 'email', 'phone']
        self.assertSequenceEqual(lista, list(form.fields))


class SubscribePostTest(TestCase):
    def setUp(self) -> None:
        self.dados = {'name': 'Eli Júnior',
                      'cpf': '00000000191',
                      'email': 'realelijr@gmail.com',
                      'phone': '61982110800',
                      }
        self.resp = self.client.post('/inscricao/', self.dados)
        self.email = mail.outbox[0]

    def test_post(self):
        """Valid POST should redirect to /inscricao/"""
        self.assertEqual(302, self.resp.status_code)

    def test_send_subscribe(self):
        self.assertEqual(1, len(mail.outbox))

    def test_subscription_email_subject(self):
        expect = 'Confirmação de Inscrição'
        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        expect = 'contato@eventex.com.br'
        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        expect = ['contato@eventex.com.br', 'realelijr@gmail.com']
        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):
        for dado in self.dados.values():
            self.assertIn(dado, self.email.body)


class SubscribeInvalidPost(TestCase):
    def setUp(self) -> None:
        self.resp = self.client.post('/inscricao/', {})
        self.form = self.resp.context['form']

    def test_post(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        self.assertIsInstance(self.form, SubscriptionForm)

    def test_form_has_errors(self):
        self.assertTrue(self.form.errors)

class SubscribeSuccessMessage(TestCase):
    def setUp(self) -> None:
        self.dados = {'name': 'Eli Júnior',
                      'cpf': '00000000191',
                      'email': 'realelijr@gmail.com',
                      'phone': '61982110800',
                      }
        self.resp = self.client.post('/inscricao/', self.dados, follow=True)

    def test_message(self):
        self.assertContains(self.resp, 'Inscrição Realizada com Sucesso!')
