
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from paypal.standard.forms import PayPalPaymentsForm
from django.shortcuts import redirect
from django.views.generic import FormView, CreateView
from .models import Freelancer, Business, Thread, Response
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


class BusinessView(FormView):
    template_name = 'accounts/signup.html'
    form_class = BusinessForm

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        return super().form_valid(form)


class FreelancerCreate(CreateView):
    form_class = FreelancerForm
    template_name = 'accounts/signup.html'
    success_url = '/accounts/login'


class BusinessCreate(CreateView):
    form_class = BusinessForm
    template_name = 'accounts/signup.html'
    success_url = '/accounts/login'

    def get_context_data(self, **kwargs):
        context = super(BusinessCreate,self).get_context_data(**kwargs)
        context['type'] = 'business'
        return context


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

def threadDetail(request, thread_id):
        thread = get_object_or_404(Thread, pk=thread_id)
       # responses = Response.objects.filter(Response_thread_title=thread_title)
        return render(request, 'threadDetail.html',{'thread':thread})

