from eventex.subscriptions.forms import SubscriptionForm
from django.shortcuts import render


def subscribe(request):
    context = {'form': SubscriptionForm()}
    return render(request, 'subscriptions/subscription_form.html', context)
