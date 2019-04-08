
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
from django.http import HttpResponse


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
    if request.user.is_superuser or request.user.is_staff:
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
        if checkUser(self.request) != 'business':
            return handler500(self.request)
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
            return handler500(request)


def threadDetail(request, thread_id):
    if checkUser(request)!='business' and checkUser(request)!='manager':
        return handler500(request)
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
        try:
            manager = Manager.objects.select_related('profile').get(id=profile.manager.id)
            return manager
        except:
            print('Principal is not a manager.')
        
    return None

def freelancerDetail(request, id):
    userString = checkUser(request)
    if userString == 'none':
        return handler500(request)
    elif userString=='freelancer':
        if id == '-':
            freelancer = findByPrincipal(request)
        else:
            freelancer = get_object_or_404(Freelancer,pk=id)
            user = findByPrincipal(request)        
            if user.id != freelancer.id:
                return handler500(request)
    else:
        if id=='-':
            return handler500(request)
        else:
            freelancer = get_object_or_404(Freelancer,pk=id)
    
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
    if checkUser(request)!='business' and checkUser(request)!='manager':
        return handler500(request)
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
        return handler500(request)
    return render(request, 'thread/threadList.html',{'threads':threads,'businessThread':businessThread})

def jobOfferList(request):
    if checkUser(request)!='freelancer' and checkUser(request)!='business' and checkUser(request)!='manager':
        return handler500(request)
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
    if checkUser(request)!='business':
        return handler500(request)
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
        return handler500(request)
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
        try:
            manager = Manager.objects.select_related('profile').get(id=profile.manager.id)
        except:
            print('Principal is not a manager.')
    if freelancer!=None:
        return 'freelancer'
    elif business !=None:
        return 'business'
    elif manager !=None:
        return 'manager'
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
    if checkUser(request) == 'business':
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
    else:
        return handler500(request)

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
        return handler500(request)

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
        return handler500(request)

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
        return handler500(request)

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
        return handler500(request)

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
        return handler500(request)

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
        return handler500(request)

def html5Edit(request, id): 
    if checkUser(request)!='freelancer' and checkUser(request)!='manager':
        return handler500(request)

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
    if checkUser(request)!='freelancer' and checkUser(request)!='manager':
        return handler500(request)

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
    if checkUser(request)!='freelancer' and checkUser(request)!='manager':
        return handler500(request)

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
    if checkUser(request)!='freelancer' and checkUser(request)!='manager':
        return handler500(request)

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
    if checkUser(request)!='freelancer' and checkUser(request)!='manager':
        return handler500(request)

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
    if checkUser(request)!='freelancer' and checkUser(request)!='manager':
        return handler500(request)

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
    if checkUser(request)!='freelancer' and checkUser(request)!='manager':
        return handler500(request)

    instance = get_object_or_404(HTML5Showcase, id=id)
    freelancer = findByPrincipal(request)
    if instance.curriculum.id != freelancer.curriculum.id:
        return render(request, 'index.html')
    instance.embedCode=""
    instance.save()
    return redirect('/freelancer/detail/'+str(freelancer.id))

def formationDelete(request, id): 
    if checkUser(request)!='freelancer' and checkUser(request)!='manager':
        return handler500(request)
    instance = get_object_or_404(Formation, id=id)
    freelancer = findByPrincipal(request)
    if instance.curriculum.id != freelancer.curriculum.id:
        return render(request, 'index.html')
    instance.delete()
    return redirect('/freelancer/detail/'+str(freelancer.id))

def professionalExperienceDelete(request, id): 
    if checkUser(request)!='freelancer' and checkUser(request)!='manager':
        return handler500(request)
    instance = get_object_or_404(ProfessionalExperience, id=id)
    freelancer = findByPrincipal(request)
    if instance.curriculum.id != freelancer.curriculum.id:
        return render(request, 'index.html')
    instance.delete()
    return redirect('/freelancer/detail/'+str(freelancer.id))

def aptitudeDelete(request, id): 
    if checkUser(request)!='freelancer' and checkUser(request)!='manager':
        return handler500(request)
    instance = get_object_or_404(Aptitude, id=id)
    freelancer = findByPrincipal(request)
    if instance.curriculum.id != freelancer.curriculum.id:
        return render(request, 'index.html')
    instance.delete()
    return redirect('/freelancer/detail/'+str(freelancer.id))

def graphicEngineExperienceDelete(request, id): 
    if checkUser(request)!='freelancer' and checkUser(request)!='manager':
        return handler500(request)
    instance = get_object_or_404(GraphicEngineExperience, id=id)
    freelancer = findByPrincipal(request)
    if instance.curriculum.id != freelancer.curriculum.id:
        return render(request, 'index.html')
    instance.delete()
    return redirect('/freelancer/detail/'+str(freelancer.id))

def linkDelete(request, id): 
    if checkUser(request)!='freelancer' and checkUser(request)!='manager':
        return handler500(request)
    instance = get_object_or_404(Link, id=id)
    freelancer = findByPrincipal(request)
    if instance.curriculum.id != freelancer.curriculum.id:
        return render(request, 'index.html')
    instance.delete()
    return redirect('/freelancer/detail/'+str(freelancer.id))

def challengeList(request):
    if(request.GET.__contains__('search')):
        search=request.GET.get('search')
        try:
            q=Challenge.objects.filter(Q(business__profile__name__icontains=search)|Q(title__icontains=search))
            challenges = get_list_or_404(q)
        except:
            challenges=()
    else:
        q=Challenge.objects.all()
    challenges= q
    return render(request, 'challenge/challengeList.html',{'challenges':challenges})

def challengeCreate(request):
    if checkUser(request)=='business':
        business = findByPrincipal(request)
        if request.method == 'POST':
            form = ChallengeForm(request.POST)
            if form.is_valid():                
                obj = form.save(commit=False)
                obj.business = business
                obj.save()
                print('Challenge saved')
                return redirect('/challenge/list/')
            else:
                return render(request,'business/standardForm.html',{'form':form,'title':'Add Challenge'})
        else:
            form = ChallengeForm()
            return render(request,'business/standardForm.html',{'form':form,'title':'Add Challenge'})
    else:
        return render(request, 'index.html')

def challengeResponse_create(request, challengeId):
    if checkUser(request) == 'freelancer':
        if request.method=="POST":
            form = ChallengeResponseForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                challenge = Challenge.objects.get(id=challengeId)
                obj.freelancer= findByPrincipal(request)
                print('todo bien')
                obj.challenge = challenge
                obj.save()
                return redirect('/challenge/detail/' + str(challengeId))
        else:
            form = ChallengeResponseForm()
        return render(request,'challenge/responseCreate.html',{'form':form})
    else:
        return handler500(request)

def challengeDetail(request, challenge_id):
        challenge = get_object_or_404(Challenge, pk=challenge_id)
        responsesChallenge = challenge.challengeresponse_set.all()
        return render(request, 'challenge/challengeDetail.html', {'challenge': challenge, 'responsesChallenge': responsesChallenge})

def curriculumVerify(request, id):
    userString = checkUser(request)
    if userString!='manager':
        return handler500(request)
    curriculum = get_object_or_404(Curriculum, pk=id)
    curriculum.verified = True
    curriculum.save()
    return redirect('/freelancer/detail/' + str(curriculum.freelancer.id))

def curriculumListManager(request):
    if checkUser(request)!='manager':
        return handler500(request)
    curriculums = Curriculum.objects.all()
    aptitudes={}
    for c in curriculums:
        aptitudesList=Aptitude.objects.filter(curriculum=c.id)
        aptitudes[c.id]=list(aptitudesList)
    return render(request, 'curriculumList.html',{'curriculums':curriculums,'aptitudes':aptitudes})


def handler404(request):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)

def termsAndConditions(request):
    return render(request, "terms-and-conditions.html")

def privacyPolicy(request):
    return render(request, "privacy-policy.html")    

def eventList(request):
    if not request.user.is_authenticated:
        return handler500(request)
    if(request.GET.__contains__('search')):
        search=request.GET.get('search')
        q=Event.objects.filter( Q(location__icontains=search)|
            Q(title__icontains=search)|
            Q(description__icontains=search))
    else:
        q=Event.objects.all()
    events= q
    return render(request, 'event/eventList.html',{'events':events})

def eventCreate(request):
    if checkUser(request)=='manager':
        manager = findByPrincipal(request)
        if request.method == 'POST':
            form = EventForm(request.POST)
            if form.is_valid():                
                obj = form.save(commit=False)
                obj.manager = manager
                obj.save()
                print('Event saved')
                return redirect('/event/list/')
            else:
                return render(request,'event/standardForm.html',{'form':form})
        else:
            form = EventForm()
            return render(request,'event/standardForm.html',{'form':form})
    else:
        return handler500(request)

def eventDetail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    freelancers= event.freelancers.all()
    companies= event.companies.all()
    manager = findByPrincipal(request)
    if checkUser(request)!='manager':
        user = findByPrincipal(request)
        if(user in freelancers or user in companies):
            joining=True
        else:
            joining=False
    else:
        joining=False
    return render(request, 'event/eventDetail.html', {'event': event,'freelancers':freelancers,'companies':companies, 'joining':joining})

def eventEdit(request, event_id): 
    if checkUser(request)!='manager':
        return handler500(request)

    instance = get_object_or_404(Event, id=event_id)
    manager = findByPrincipal(request)

    form = EventForm(request.POST or None, instance=instance)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.manager = manager
        obj.save()
        return redirect('/event/detail/'+str(event_id))
    return render(request,'event/standardForm.html',{'form':form})

def eventJoin(request, event_id): 
    userRole=checkUser(request)
    if userRole!='business' and userRole!='freelancer':
        return handler500(request)
    instance = get_object_or_404(Event, id=event_id)
    user = findByPrincipal(request)

    form = EventForm(instance=instance)
    obj = form.save(commit=False)
    if userRole=='freelancer':
        obj.freelancers.add(user)
    else:
        obj.companies.add(user)
    obj.save()
    return redirect('/event/detail/'+str(event_id))