
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, get_list_or_404
from paypal.standard.forms import PayPalPaymentsForm
from django.shortcuts import redirect
from django.views.generic import FormView, CreateView
from .models import Freelancer, Business, Thread, Response, Link
from .forms import FreelancerForm, BusinessForm, ThreadForm


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


def login_redir(request):
    if request.user.is_superuser:
        res = redirect('admin/')
    else:
        res = redirect('accounts/login/')
    return res


class FreelancerView(FormView):
    template_name = 'accounts/signup.html'
    form_class = FreelancerForm

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        print('form_valid')
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

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        print('FreelancerCreate: form_valid')

        return super().form_valid(form)


class BusinessCreate(CreateView):
    form_class = BusinessForm
    template_name = 'accounts/signup.html'
    success_url = '/accounts/login'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        print('BusinessCreate: form_valid')

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # This method is called before the view es generate and add the context
        # It should return the context

        context = super(BusinessCreate,self).get_context_data(**kwargs)
        context['type'] = 'business'
        return context


class ThreadCreate(CreateView):
    form_class = ThreadForm
    template_name = 'thread/form.html'
    success_url = '/accounts/login'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        print('ThreadCreate: form_valid')

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # This method is called before the view es generate and add the context
        # It should return the context

        context = super(ThreadCreate, self).get_context_data(**kwargs)

        return context


def threadDetail(request, thread_id):
        thread = get_object_or_404(Thread, pk=thread_id)
        responses = thread.response_set.all()
        return render(request, 'threadDetail.html', {'thread': thread, 'responses:': responses})

def freelancerDetail(request, id):
        freelancer = get_object_or_404(Freelancer, pk=id)
        #links = Link.objects.select_related('freelancer').get(id=id)
        links = freelancer.link_set.all()
        return render(request, 'freelancer/detail.html', {'freelancer': freelancer,'links':links})

def threadList(request, business_id):
    if(request.GET.__contains__('search')):
        search=request.GET.get('search')
        q=Thread.objects.filter(business=business_id).filter(business__profile__name__icontains=search)
    else:
        q=Thread.objects.filter(business=business_id)
    threads= get_list_or_404(q)
    businessThread= get_object_or_404(Business,pk=business_id)
    return render(request, 'threadList.html',{'threads':threads,'businessThread':businessThread})   