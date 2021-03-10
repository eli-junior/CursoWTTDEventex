from eventex.subscriptions.forms import SubscriptionForm
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.conf import settings
from django.core import mail


def subscribe(request):
    if request.method == 'POST':
        return create(request)
    else:
        return new(request)


def create(request):
    form = SubscriptionForm(request.POST)
    if not form.is_valid():
        return render(request, 'subscriptions/subscription_form.html', {'form': form})

    _send_mail(template_name='subscriptions/subscription_email.txt',
               context=form.cleaned_data,
               subject='Confirmação de Inscrição',
               from_=settings.DEFAULT_FROM_EMAIL,
               to=form.cleaned_data['email'])

    messages.success(request, 'Inscrição Realizada com Sucesso!')

    return HttpResponseRedirect('/inscricao/')


def new(request):
    return render(request, 'subscriptions/subscription_form.html', {'form': SubscriptionForm()})


def _send_mail(subject, from_, to, template_name, context):
    body = render_to_string(template_name, context)
    mail.send_mail(subject=subject, message=body, from_email=from_, recipient_list=[from_, to])
