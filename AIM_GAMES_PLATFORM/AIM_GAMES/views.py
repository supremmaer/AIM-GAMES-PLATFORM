
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, get_list_or_404
from paypal.standard.forms import PayPalPaymentsForm
from django.shortcuts import redirect
from django.views.generic import FormView, CreateView
from .models import Freelancer, Business, Thread, Response, Link, JobOffer, Curriculum, Profile
from .forms import FreelancerForm, BusinessForm, ThreadForm
from django.db.models import Q
from datetime import datetime, timezone
from django.contrib import auth
from django.contrib import sessions
from django.contrib.auth.models import Group

from django.utils.translation import gettext as _
from django.utils import translation

def index(request):
    # esto es como el controlador/servicios
    if not request.session.has_key('language'):
        request.session['language'] = 'es-ES'
    language = request.session['language']
    translation.activate(language)

    return render(request, 'index.html')

def setlanguage(request, language):
    request.session['language'] = language
    return redirect('/')

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
    return render(request, 'pagarPaypal.html', {'form':form})

    
def payment_done(request):
    # esto es como el controlador/servicios
    buss_id = request.session.get('buss')
    Business.objects.filter(id=buss_id).update(lastPayment=datetime.now())
    return render(request, 'payment_done.html')


def payment_canceled(request):
    # esto es como el controlador/servicios
    return render(request, 'payment_canceled.html')


def login_redir(request):
    if request.user.is_superuser:
        res = redirect('admin/')
    else:
        prof = Profile.objects.filter(user__pk=request.user.id)
        buss = Business.objects.filter(profile__pk=prof[0].id)
        if buss:
            if not buss[0].lastPayment is None:
                if (buss[0].lastPayment- datetime.now(timezone.utc)).total_seconds() > 31556952:
                    auth.logout(request)
                    res = pagarPaypal(request)
                else:
                    res = redirect('accounts/login/')
            else:
                auth.logout(request)
                res = pagarPaypal(request)
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

    def __init__(self, *args, **kwargs):
        super(BusinessCreate, self).__init__(*args, **kwargs)

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        print('BusinessCreate: form_valid')

        #
        buss = form.save()
        print(buss)

        self.request.session['buss'] = buss.id
        return pagarPaypal(self.request)

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
        print(form.cleaned_data)

        return render(threadDetail(self.request,1))

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
        freelancer = get_object_or_404(Freelancer,pk=id)
        curriculum = freelancer.curriculum
        links = curriculum.link_set.all()
        formation = curriculum.formation_set.all()
        professionalExperience = curriculum.professionalexperience_set.all()
        HTML5Showcase = curriculum.html5showcase_set.all()
        graphicEngineExperience = curriculum.graphicengineexperience_set.all()
        aptitude = curriculum.aptitude_set.all()
        return render(request, 'freelancer/detail.html', {'freelancer': freelancer,'links':links,'formations':formation,'professionalExperiences':professionalExperience,'HTML5Showcase':HTML5Showcase,'graphicEngineExperiences':graphicEngineExperience,'aptitudes':aptitude})

def threadList(request, business_id):
    if(request.GET.__contains__('search')):
        search=request.GET.get('search')
        q=Thread.objects.filter(business=business_id).filter(business__profile__name__icontains=search)
    else:
        q=Thread.objects.filter(business=business_id)
    queryset = _get_queryset(q)
    queryset2 = _get_queryset(Business)
    threads= list(queryset)
    businessThread= queryset2.get(pk=business_id)
    return render(request, 'threadList.html',{'threads':threads,'businessThread':businessThread}) 

def jobOfferList(request):
    if(request.GET.__contains__('search')):
        search=request.GET.get('search')
        q=JobOffer.objects.filter( Q(business__profile__name__icontains=search)|
        Q(position__icontains=search)|
        Q(experienceRequired__icontains=search)|
        Q(ubication__icontains=search)|
        Q(description__icontains=search))
    else:
        q=JobOffer.objects.all()
    jobOffers= get_list_or_404(q)
    return render(request, 'jobOfferList.html',{'jobOffers':jobOffers}) 

def checkUser(request):
    freelancer = None
    business = None
    if request.user.is_authenticated:
        user = request.user
        profile = user.profile
        print(profile)
        #profile = Profile.objects.select_related('user').get(id=user.id)
        try:
            freelancer = Freelancer.objects.select_related('profile').get(id=profile.freelancer.id)
        except:
            print('magic')
        try:
            business = Business.objects.select_related('profile').get(id=profile.business.id)
        except:
            print('moar magic')
    if freelancer!=None:
        return 'freelancer'
    elif business !=None:
        return 'bussines'
    else:
        return 'none'

def _get_queryset(klass):
    """
    Return a QuerySet or a Manager.
    Duck typing in action: any class with a `get()` method (for
    get_object_or_404) or a `filter()` method (for get_list_or_404) might do
    the job.
    """
    # If it is a model class or anything else with ._default_manager
    if hasattr(klass, '_default_manager'):
        return klass._default_manager.all()
    return klass