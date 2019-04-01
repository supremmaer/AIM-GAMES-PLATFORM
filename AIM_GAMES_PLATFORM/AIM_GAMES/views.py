
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, get_list_or_404
from paypal.standard.forms import PayPalPaymentsForm
from django.shortcuts import redirect
from django.views.generic import FormView, CreateView, UpdateView
from .models import Freelancer, Business, Thread, Response, Link, JobOffer, Curriculum, Profile, Aptitude
from .forms import *
from django.db.models import Q
from datetime import datetime, timezone
from django.contrib import auth
from django.contrib import sessions
from django.contrib.auth.models import Group
from django.http import Http404


from django.utils.translation import gettext as _
from django.utils import translation

def index(request):
    # esto es como el controlador/servicios
    try:
        request.session['currentUser'] = checkUser(request)
    except:
        request.session['currentUser'] ='none'

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
                    res = redirect('index')
            else:
                auth.logout(request)
                res = pagarPaypal(request)
        else:
            res = redirect('index')

    try:
        request.session['currentUser'] = checkUser(request)
    except:
        request.session['currentUser'] ='none'

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

        prof = Profile.objects.filter(user__pk=self.request.user.id)
        buss = Business.objects.filter(profile__pk=prof[0].id)
        thread = form.save(buss)

        return threadDetail(self.request, thread.id)

    def get_context_data(self, **kwargs):
        # This method is called before the view es generate and add the context
        # It should return the context

        context = super(ThreadCreate, self).get_context_data(**kwargs)

        return context

    def dispatch(self, request, *args, **kwargs):
        if checkUser(self.request) == 'business':
            return super(ThreadCreate, self).dispatch(request, *args, **kwargs)
        else:
            redirect('accounts/login')


def threadDetail(request, thread_id):
        thread = get_object_or_404(Thread, pk=thread_id)
        responses = thread.response_set.all()
        pics = thread.pics
        return render(request, 'thread/threadDetail.html', {'thread': thread, 'responses': responses,'pics':pics})

def jobOfferDetail(request, id):
        jobOffer = get_object_or_404(JobOffer, pk=id)
        pics = jobOffer.images.split(",")
        for pic in pics:
            pic.strip()
        
        return render(request, 'jobOfferDetail.html', {'jobOffer': jobOffer, 'pics' : pics})


def freelancerDetail(request, id):
        if id!='-':
            freelancer = get_object_or_404(Freelancer,pk=id)
            if checkUser(request)=='freelancer':
                freelancer = findByPrincipal(request)
                if(freelancer.id!=id):
                    return render(request, 'index.html')
        else:
            freelancer = findByPrincipal(request)
        curriculum = freelancer.curriculum
        links = curriculum.link_set.all()
        formation = curriculum.formation_set.all()
        professionalExperience = curriculum.professionalexperience_set.all()
        graphicEngineExperience = curriculum.graphicengineexperience_set.all()
        aptitude = curriculum.aptitude_set.all()
        try:
            HTML5Showcase = curriculum.HTML5Showcase
        except:
            HTML5Showcase = None

        return render(request, 'freelancer/detail.html', {'freelancer': freelancer,'links':links,'formations':formation,'professionalExperiences':professionalExperience,'HTML5Showcase':HTML5Showcase,'graphicEngineExperiences':graphicEngineExperience,'aptitudes':aptitude})

def threadList(request):
    if(request.GET.__contains__('search')):
        search=request.GET.get('search')
        q=Thread.objects.filter(business__profile__name__icontains=search)
    else:
        q=Thread.objects.all()
    threads= q
    #Esta llamada sirve también como comprobación de si la llamada se hace desde una URL que no es de business
    try:
        businessThread = get_object_or_404(Business,profile=request.user.profile)
    except AttributeError:
        raise Http404('Debe estar autentificado como empresa para acceder a este servicio')
    return render(request, 'thread/threadList.html',{'threads':threads,'businessThread':businessThread})

def jobOfferList(request):
    
    if(request.GET.__contains__('search')):
        search=request.GET.get('search')
        try:
            q=JobOffer.objects.filter( Q(business__profile__name__icontains=search)|
            Q(position__icontains=search)|
            Q(experienceRequired__icontains=search)|
            Q(ubication__icontains=search)|
            Q(description__icontains=search))
            jobOffers= get_list_or_404(q)
        except:
            jobOffers=()
    else:
        q=JobOffer.objects.all()
    jobOffers= q
    return render(request, 'jobOfferList.html',{'jobOffers':jobOffers})

def curriculumList(request):
    if(request.GET.__contains__('search')):
        search=request.GET.get('search')
        q=Curriculum.objects.filter(freelancer__profile__name__icontains=search)
    else:
        q=Curriculum.objects.all()
    curriculums= q
    aptitudes={}
    for c in curriculums:
        aptitudesList=Aptitude.objects.filter(curriculum=c.id)
        aptitudes[c.id]=list(aptitudesList)
    try:
        businessThread = get_object_or_404(Business,profile=request.user.profile)
    except AttributeError:
        raise Http404('Debe estar autentificado como empresa para acceder a este servicio')
    return render(request, 'curriculumList.html',{'curriculums':curriculums,'aptitudes':aptitudes})

def checkUser(request):
    freelancer = None
    business = None
    if request.user.is_authenticated:
        user = request.user
        try:
            profile = user.profile
        except:
            return 'admin'
        try:
            freelancer = Freelancer.objects.select_related('profile').get(id=profile.freelancer.id)
        except:
            print('Principal is not a freelancer.')
        try:
            business = Business.objects.select_related('profile').get(id=profile.business.id)
        except:
            print('Principal is not a business.')
    if freelancer!=None:
        return 'freelancer'
    elif business !=None:
        return 'business'
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

def response_create(request, threadId):
    if request.method=="POST":
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            userprofile = Profile.objects.get(user=request.user)
            businessPrincipal = Business.objects.get(profile=userprofile)
            response.business=businessPrincipal
            thread = Thread.objects.get(id=threadId) 
            response.thread = thread
            response.save()
            return redirect('/thread/detail/' + str(threadId))
    else:
        form = ResponseForm()
    return render(request,'thread/responseCreate.html',{'form':form})

def findByPrincipal(request):
    freelancer = None
    business = None
    if request.user.is_authenticated:
        user = request.user
        try:
            profile = user.profile
        except:
            print('admin logged')
        try:
            freelancer = Freelancer.objects.select_related('profile').get(id=profile.freelancer.id)
            return freelancer
        except:
            print('Principal is not a freelancer.')
        try:
            business = Business.objects.select_related('profile').get(id=profile.business.id)
            return business
        except:
            print('Principal is not a business.')
    return None

def linkCreate(request):
    if checkUser(request)=='freelancer':
        freelancer = findByPrincipal(request)
        if request.method == 'POST':
            form = LinkForm(request.POST)
            if form.is_valid():                
                link = form.save(commit=False)
                link.curriculum = freelancer.curriculum
                link.save()
                print('link saved')
                return redirect('/freelancer/detail/'+str(freelancer.id))
        else:
            form = LinkForm()
            return render(request,'freelancer/standardForm.html',{'form':form,'title':'Add link'})
    else:
        return render(request, 'index.html')

def aptitudeCreate(request):
    if checkUser(request)=='freelancer':
        freelancer = findByPrincipal(request)
        if request.method == 'POST':
            form = AptitudeForm(request.POST)
            if form.is_valid():                
                obj = form.save(commit=False)
                obj.curriculum = freelancer.curriculum
                obj.save()
                print('Aptitude saved')
                return redirect('/freelancer/detail/'+str(freelancer.id))
            else:
                return render(request,'freelancer/standardForm.html',{'form':form,'title':'Add aptitude'})
        else:
            form = AptitudeForm()
            return render(request,'freelancer/standardForm.html',{'form':form,'title':'Add aptitude'})
    else:
        return render(request, 'index.html')

def graphicEngineExperienceCreate(request):
    if checkUser(request)=='freelancer':
        freelancer = findByPrincipal(request)
        if request.method == 'POST':
            form = GraphicEngineExperienceForm(request.POST)
            if form.is_valid():                
                obj = form.save(commit=False)
                obj.curriculum = freelancer.curriculum
                obj.save()
                print('Graphic engine experience saved')
                return redirect('/freelancer/detail/'+str(freelancer.id))
            else:
                return render(request,'freelancer/standardForm.html',{'form':form,'title':'Add graphic engine experience'})
        else:
            form = GraphicEngineExperienceForm()
            return render(request,'freelancer/standardForm.html',{'form':form,'title':'Add graphic engine experience'})
    else:
        return render(request, 'index.html')

def professionalExperienceCreate(request):
    if checkUser(request)=='freelancer':
        freelancer = findByPrincipal(request)
        if request.method == 'POST':
            form = ProfessionalExperienceForm(request.POST)
            if form.is_valid():                
                obj = form.save(commit=False)
                obj.curriculum = freelancer.curriculum
                obj.save()
                print('Professional Experience saved')
                return redirect('/freelancer/detail/'+str(freelancer.id))
            else:
                return render(request,'freelancer/standardForm.html',{'form':form,'title':'Add professional experience'})
        else:
            form = ProfessionalExperienceForm()
            return render(request,'freelancer/standardForm.html',{'form':form,'title':'Add professional experience'})
    else:
        return render(request, 'index.html')

def formationCreate(request):
    if checkUser(request)=='freelancer':
        freelancer = findByPrincipal(request)
        if request.method == 'POST':
            form = FormationForm(request.POST)
            if form.is_valid():                
                obj = form.save(commit=False)
                obj.curriculum = freelancer.curriculum
                obj.save()
                print('formation saved')
                return redirect('/freelancer/detail/'+str(freelancer.id))
            else:
                return render(request,'freelancer/standardForm.html',{'form':form,'title':'Add formation'})
        else:
            form = FormationForm()
            return render(request,'freelancer/standardForm.html',{'form':form,'title':'Add formation'})
    else:
        return render(request, 'index.html')

def jobOfferCreate(request):
    if checkUser(request)=='business':
        business = findByPrincipal(request)
        if request.method == 'POST':
            form = JobOfferForm(request.POST)
            if form.is_valid():                
                obj = form.save(commit=False)
                obj.business = business
                obj.save()
                print('job offer saved')
                return redirect('/joboffer/user/list/')
            else:
                return render(request,'business/standardForm.html',{'form':form,'title':'Add Job Offer'})
        else:
            form = JobOfferForm()
            return render(request,'business/standardForm.html',{'form':form,'title':'Add Job Offer'})
    else:
        return render(request, 'index.html')

def html5Edit(request, id): 
    if checkUser(request)!='freelancer':
        return render(request, 'index.html')

    instance = get_object_or_404(HTML5Showcase, id=id)
    freelancer = findByPrincipal(request)
    if instance.curriculum.id != freelancer.curriculum.id:
        return render(request, 'index.html')

    form = html5showcaseForm(request.POST or None, instance=instance)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.curriculum = freelancer.curriculum
        obj.save()
        return redirect('/freelancer/detail/'+str(freelancer.id))
    return render(request,'freelancer/standardForm.html',{'form':form,'title':'Edit HTML5Showcase'})

def formationEdit(request, id): 
    if checkUser(request)!='freelancer':
        return render(request, 'index.html')

    instance = get_object_or_404(Formation, id=id)
    freelancer = findByPrincipal(request)
    if instance.curriculum.id != freelancer.curriculum.id:
        return render(request, 'index.html')

    form = FormationForm(request.POST or None, instance=instance)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.curriculum = freelancer.curriculum
        obj.save()
        return redirect('/freelancer/detail/'+str(freelancer.id))
    return render(request,'freelancer/standardForm.html',{'form':form,'title':'Edit Formation'})

def professionalExperienceEdit(request, id): 
    if checkUser(request)!='freelancer':
        return render(request, 'index.html')

    instance = get_object_or_404(ProfessionalExperience, id=id)
    freelancer = findByPrincipal(request)
    if instance.curriculum.id != freelancer.curriculum.id:
        return render(request, 'index.html')

    form = ProfessionalExperienceForm(request.POST or None, instance=instance)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.curriculum = freelancer.curriculum
        obj.save()
        return redirect('/freelancer/detail/'+str(freelancer.id))
    return render(request,'freelancer/standardForm.html',{'form':form,'title':'Edit ProfessionalExperience'})

def aptitudeEdit(request, id): 
    if checkUser(request)!='freelancer':
        return render(request, 'index.html')

    instance = get_object_or_404(Aptitude, id=id)
    freelancer = findByPrincipal(request)
    if instance.curriculum.id != freelancer.curriculum.id:
        return render(request, 'index.html')

    form = AptitudeForm(request.POST or None, instance=instance)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.curriculum = freelancer.curriculum
        obj.save()
        return redirect('/freelancer/detail/'+str(freelancer.id))
    return render(request,'freelancer/standardForm.html',{'form':form,'title':'Edit Aptitude'})

def graphicEngineExperienceEdit(request, id): 
    if checkUser(request)!='freelancer':
        return render(request, 'index.html')

    instance = get_object_or_404(GraphicEngineExperience, id=id)
    freelancer = findByPrincipal(request)
    if instance.curriculum.id != freelancer.curriculum.id:
        return render(request, 'index.html')

    form = GraphicEngineExperienceForm(request.POST or None, instance=instance)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.curriculum = freelancer.curriculum
        obj.save()
        return redirect('/freelancer/detail/'+str(freelancer.id))
    return render(request,'freelancer/standardForm.html',{'form':form,'title':'Edit Graphic Engine Experience'})

def linkEdit(request, id): 
    if checkUser(request)!='freelancer':
        return render(request, 'index.html')

    instance = get_object_or_404(Link, id=id)
    freelancer = findByPrincipal(request)
    if instance.curriculum.id != freelancer.curriculum.id:
        return render(request, 'index.html')

    form = LinkForm(request.POST or None, instance=instance)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.curriculum = freelancer.curriculum
        obj.save()
        return redirect('/freelancer/detail/'+str(freelancer.id))
    return render(request,'freelancer/standardForm.html',{'form':form,'title':'Edit Link'})

def html5Delete(request, id): 
    if checkUser(request)!='freelancer':
        return render(request, 'index.html')

    instance = get_object_or_404(HTML5Showcase, id=id)
    freelancer = findByPrincipal(request)
    if instance.curriculum.id != freelancer.curriculum.id:
        return render(request, 'index.html')
    instance.embedCode=""
    instance.save()
    return redirect('/freelancer/detail/'+str(freelancer.id))

def formationDelete(request, id): 
    if checkUser(request)!='freelancer':
        return render(request, 'index.html')
    instance = get_object_or_404(Formation, id=id)
    freelancer = findByPrincipal(request)
    if instance.curriculum.id != freelancer.curriculum.id:
        return render(request, 'index.html')
    instance.delete()
    return redirect('/freelancer/detail/'+str(freelancer.id))

def professionalExperienceDelete(request, id): 
    if checkUser(request)!='freelancer':
        return render(request, 'index.html')
    instance = get_object_or_404(ProfessionalExperience, id=id)
    freelancer = findByPrincipal(request)
    if instance.curriculum.id != freelancer.curriculum.id:
        return render(request, 'index.html')
    instance.delete()
    return redirect('/freelancer/detail/'+str(freelancer.id))

def aptitudeDelete(request, id): 
    if checkUser(request)!='freelancer':
        return render(request, 'index.html')
    instance = get_object_or_404(Aptitude, id=id)
    freelancer = findByPrincipal(request)
    if instance.curriculum.id != freelancer.curriculum.id:
        return render(request, 'index.html')
    instance.delete()
    return redirect('/freelancer/detail/'+str(freelancer.id))

def graphicEngineExperienceDelete(request, id): 
    if checkUser(request)!='freelancer':
        return render(request, 'index.html')
    instance = get_object_or_404(GraphicEngineExperience, id=id)
    freelancer = findByPrincipal(request)
    if instance.curriculum.id != freelancer.curriculum.id:
        return render(request, 'index.html')
    instance.delete()
    return redirect('/freelancer/detail/'+str(freelancer.id))

def linkDelete(request, id): 
    if checkUser(request)!='freelancer':
        return render(request, 'index.html')
    instance = get_object_or_404(Link, id=id)
    freelancer = findByPrincipal(request)
    if instance.curriculum.id != freelancer.curriculum.id:
        return render(request, 'index.html')
    instance.delete()
    return redirect('/freelancer/detail/'+str(freelancer.id))