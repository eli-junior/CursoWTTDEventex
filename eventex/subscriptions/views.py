import uuid

from django.conf import settings
from django.core import mail
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template.loader import render_to_string

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


def subscribe(request):
    if request.method == 'POST':
        return create(request)
    else:
        return new(request)


def create(request):
    form = SubscriptionForm(request.POST)
    if not form.is_valid():
        return render(request, 'subscriptions/subscription_form.html', {'form': form})

    # Create a aleatory ID for subscription
    id_ = str(uuid.uuid4()).replace('-', '')
    subscription = Subscription.objects.create(id=id_, **form.cleaned_data)

    if settings.SEND_EMAIL:
        _send_mail(
            template_name='subscriptions/subscription_email.txt',
            subject='Confirmação de Inscrição',
            from_=settings.DEFAULT_FROM_EMAIL,
            to=subscription.email,
            context={'subscription': subscription}
        )

    return HttpResponseRedirect('/inscricao/%s/' % subscription.pk)


def new(request):
    return render(
        request,
        'subscriptions/subscription_form.html',
        {'form': SubscriptionForm()}
    )


def detail(request, pk):
    try:
        subscription = Subscription.objects.get(pk=pk)

    except Subscription.DoesNotExist:
        raise Http404

    else:
        return render(
            request,
            'subscriptions/subscription_detail.html',
            {'subscription': subscription}
        )


def _send_mail(subject, from_, to, template_name, context):
    body = render_to_string(template_name, context)
    mail.send_mail(subject=subject, message=body, from_email=from_, recipient_list=[from_, to])
