
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from paypal.standard.forms import PayPalPaymentsForm
from django.shortcuts import redirect
from django.views.generic import FormView, CreateView
from AIM_GAMES.models import Freelancer, Business

# Create your views here.
from django.http import HttpResponse

from .forms import FreelancerForm, BusinessForm


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


class FreelancerView(FormView):
    template_name = 'accounts/signup.html'
    form_class = FreelancerForm

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        return super().form_valid(form)


class FreelancerCreate(CreateView):

    model = Freelancer
    fields = ['profile','profession']


# def signup(request):
#     if request.method == 'POST':
#         # Do things
#         form = SignupForm(request.POST)
#     else:
#         if request.GET.get('b') == "1":
#             context = {'type': "business"}
#         else:
#             context = {'type': "user"}
#     return render(request, 'signup/signup.html', context)


