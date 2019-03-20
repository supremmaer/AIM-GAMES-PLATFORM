
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from paypal.standard.forms import PayPalPaymentsForm

# Create your views here.
from django.http import HttpResponse

from .forms import SignupForm, LoginForm
from .models import Profile
from django.contrib.auth import authenticate


def index(request):
    # esto es como el controlador/servicios
    return render(request, 'index.html')


def pagarPaypal(request):
    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '71',
        'item_name': 'Subscripcion AIM-GAMES',
        'currency_code': 'EUR',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host, reverse('payment_canceled')),
        }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'pagarPaypal.html', {'form': form })

    
def payment_done(request):
    # esto es como el controlador/servicios
    return render(request, 'payment_done.html')


def payment_canceled(request):
    # esto es como el controlador/servicios
    return render(request, 'payment_canceled.html')


def login(request):
    if request.method == 'POST':
        # Do things
        print(str(request.POST))
        form = LoginForm(request.POST)
        if form.is_valid():
            print('Valid form: '+str(form.cleaned_data))
            user = authenticate(username=form.cleaned_data.get('user'), password=form.cleaned_data.get('password'))
            res = render(request, 'login/login.html', {'form': form,'usuario':user})
        else:
            print('Invalid form: '+str(form.cleaned_data))
            res = render(request, 'login/login.html', {'form': form})
    else:
        print('New form')
        form = LoginForm()
        res = render(request, 'login/login.html', {'form': form})
    return res;


def signup(request):
    if request.method == 'POST':
        # Do things
        form = SignupForm(request.POST)
    else:
        if request.GET.get('b') == "1":
            context = {'type': "business"}
        else:
            context = {'type': "user"}
    return render(request, 'signup/signup.html', context)

