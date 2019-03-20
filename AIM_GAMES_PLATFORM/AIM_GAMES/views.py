
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from paypal.standard.forms import PayPalPaymentsForm
from django.shortcuts import redirect

# Create your views here.
from django.http import HttpResponse

from .forms import SignupForm
from .models import Thread, Response


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


def loginRedir(request):
    if request.user.is_superuser:
        res = redirect('admin/')
    else:
        res = redirect('accounts/login/')
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

def threadDetail(request, thread_id):
        thread = get_object_or_404(Thread, pk=thread_id)
       # responses = Response.objects.filter(Response_thread_title=thread_title)
        return render(request, 'threadDetail.html',{'thread':thread})