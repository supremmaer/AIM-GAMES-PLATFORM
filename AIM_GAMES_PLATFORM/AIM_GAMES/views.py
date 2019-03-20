
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from paypal.standard.forms import PayPalPaymentsForm

# Create your views here.
from django.http import HttpResponse

from .forms import SignupForm
from .models import Profile

##LOGIN VIEW
from django.conf import settings
# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, login as auth_login
)
from django.contrib.auth.forms import (
    AuthenticationForm
)
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.edit import FormView

##END OF LOGIN VIEW

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

'''
def login(request):
    if request.method == 'POST':
        # Do things
        print(str(request.POST))
        form = LoginForm(request.POST)
        if form.is_valid():
            print('Valid form: '+str(form.cleaned_data))
            user = authenticate(request, username=form.cleaned_data.get('user'), password=form.cleaned_data.get('password'))
            res = render(request, 'login/login.html', {'form': form,'usuario':user})
        else:
            print('Invalid form: '+str(form.cleaned_data))
            res = render(request, 'login/login.html', {'form': form})
    else:
        print('New form')
        form = LoginForm()
        res = render(request, 'login/login.html', {'form': form})
    return res;

'''
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


