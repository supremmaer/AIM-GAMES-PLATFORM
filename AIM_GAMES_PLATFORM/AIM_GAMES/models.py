from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.utils.translation import ugettext_lazy as _

# Create your models here.
# System objects


class Tag(models.Model):
    title = models.TextField(verbose_name=_(
        "title"), max_length=20, primary_key=True, blank=False)

    def __str__(self):
        return self.title


class GraphicEngine(models.Model):
    title = models.TextField(verbose_name=_(
        "title"), max_length=50, primary_key=True, blank=False)

    def __str__(self):
        return self.title


# Misc


class URL(models.Model):
    uri = models.URLField(verbose_name=_("uri"),default='http://default.com')

    def __str__(self):
        return self.uri


# Profile class. Attributes regarding all users of the system go here


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name=_("user"))
    name = models.TextField(verbose_name=_("name"), max_length=30, blank=False)
    surname = models.TextField(verbose_name=_(
        "surname"), max_length=50, blank=False)
    email = models.EmailField(verbose_name=_("email"), blank=False)
    city = models.TextField(verbose_name=_("city"), max_length=30, blank=False)
    postalCode = models.TextField(verbose_name=_(
        "Postal Code"), max_length=16, blank=False)
    idCardNumber = models.TextField(verbose_name=_(
        "IDCard Number"), max_length=10, blank=False)
    dateOfBirth = models.DateTimeField(
        verbose_name=_("Date of birth"), null=False)
    phoneNumber = models.TextField(verbose_name=_(
        "Phone number"), max_length=20, blank=False)
    photo = models.URLField(verbose_name=_("Photo"))

    def __str__(self):
        return self.name


# Types of users


class Freelancer(models.Model):
    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, verbose_name=_("profile"))
    profession = models.TextField(verbose_name=_("profession"), max_length=100)

    def __str__(self):
        return self.profile.email

    def get_absolute_url(self):
        return reverse('signupFreelancer', kwargs={'pk': self.pk})

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password


class Business(models.Model):
    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, verbose_name=_("profile"))
    lastPayment = models.DateTimeField(
        verbose_name=_("lastPayment"), null=True)

    def __str__(self):
        return self.profile.email


class Manager(models.Model):
    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, verbose_name=_("profile"))

    def __str__(self):
        return self.profile.email

# Freelancer objects


class Curriculum(models.Model):
    freelancer = models.OneToOneField(
        Freelancer, on_delete=models.CASCADE, verbose_name=_("freelancer"))
    verified = models.BooleanField(verbose_name=_("verified"), default=False)


class ProfessionalExperience(models.Model):
    curriculum = models.ForeignKey(
        Curriculum, on_delete=models.CASCADE, verbose_name=_("curriculum"))
    center = models.TextField(verbose_name=_(
        "center"), max_length=50, blank=False)
    formation = models.TextField(verbose_name=_(
        "formation"), max_length=100, blank=False)
    startDate = models.DateTimeField(verbose_name=_("startDate"), null=False)
    endDate = models.DateTimeField(verbose_name=_("endDate"), null=False)
    miniature = models.URLField(verbose_name=_("miniature"),)

    def getData(self):
        data = "Center: " + self.center + "\n" + "Formation: " + self.formation + "\n" + "Start date: " + \
            self.startDate.strftime('%m/%d/%Y') + "\n" + "End date: " + self.endDate.strftime(
                '%m/%d/%Y') + "\n" + "Miniature: " + self.miniature
        return data


class Formation(models.Model):
    curriculum = models.ForeignKey(
        Curriculum, on_delete=models.CASCADE, verbose_name=_("curriculum"))
    center = models.TextField(verbose_name=_(
        "center"), max_length=50, blank=False)
    formation = models.TextField(verbose_name=_(
        "formation"), max_length=100, blank=False)
    startDate = models.DateTimeField(verbose_name=_("startDate"), null=False)
    endDate = models.DateTimeField(verbose_name=_("endDate"), null=False)
    miniature = models.URLField(verbose_name=_("miniature"),)

    def getData(self):
        data = "Center: " + self.center + "\n" + "Formation: " + self.formation + "\n" + "Start date: " + \
            self.startDate.strftime('%m/%d/%Y') + "\n" + "End date: " + self.endDate.strftime(
                '%m/%d/%Y') + "\n" + "Miniature: " + self.miniature
        return data


class GraphicEngineExperience(models.Model):
    curriculum = models.ForeignKey(
        Curriculum, on_delete=models.CASCADE, verbose_name=_("curriculum"))
    graphicEngine = models.ForeignKey(
        GraphicEngine, on_delete=models.CASCADE, verbose_name=_("graphicEngine"))
    graphicExperience = models.IntegerField(verbose_name=_("graphicExperience"),
                                            validators=[MinValueValidator(0), MaxValueValidator(100)])

    def getData(self):
        data = ""
        data = "Graphic engine: " + data + \
            str(self.graphicEngine) + "\n" + \
            "Experience: " + str(self.graphicExperience)
        return data


class HTML5Showcase(models.Model):
    curriculum = models.OneToOneField(
        Curriculum, on_delete=models.CASCADE, related_name='HTML5Showcase', verbose_name=_("curriculum"))
    embedCode = models.TextField(verbose_name=_("embedCode"),)

    def getData(self):
        data = "Embed code: " + self.embedCode
        return data


class Aptitude(models.Model):
    curriculum = models.ForeignKey(
        Curriculum, on_delete=models.CASCADE, verbose_name=_("curriculum"))
    aptitude = models.TextField(verbose_name=_(
        "aptitude"), max_length=30, blank=False, default='defaul')

    def getData(self):
        data = "aptitude: " + self.aptitude
        return data


class Link(models.Model):
    curriculum = models.ForeignKey(
        Curriculum, on_delete=models.CASCADE, verbose_name=_("curriculum"))
    url = models.URLField(verbose_name=_("url"), blank=False)

    def getData(self):
        data = self.url
        return data

# Business objects


class JobOffer(models.Model):
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, verbose_name=_("business"))
    position = models.TextField(verbose_name=_(
        "position"), max_length=100, blank=False)
    experienceRequired = models.TextField(verbose_name=_(
        "experienceRequired"), max_length=100, blank=False)
    schedule = models.TextField(verbose_name=_(
        "schedule"), max_length=100, blank=False)
    salary = models.IntegerField(verbose_name=_("salary"), null=False)
    ubication = models.TextField(verbose_name=_(
        "ubication"), max_length=100, blank=False)
    description = models.TextField(verbose_name=_(
        "description"), max_length=10000, blank=False)
    images = models.TextField(verbose_name=_("images"), blank=False)

    def getData(self):
        data = "Position: " + self.position + "\n" + "Experience required: " + self.experienceRequired + "\n" + "Schedule: " + self.schedule + \
            "\n" + "Salary: " + str(self.salary) + "\n" + "Ubication: " + \
            self.ubication + "\n" + "Description: " + \
            self.description + "Images: " + self.images + "\n"
        return data


class Thread(models.Model):
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, verbose_name=_("business"))
    title = models.TextField(verbose_name=_(
        "title"), max_length=100, blank=False)
    description = models.TextField(verbose_name=_("description"), blank=False)
    tags = models.ManyToManyField(Tag, blank=True, verbose_name=_("tags"))
    pics = models.ManyToManyField(
        URL, related_name="pic", verbose_name=_("pics"))
    attachedFiles = models.ManyToManyField(
        URL, related_name="attachedFile", verbose_name=_("attachedFiles"))

    def __str__(self):
        return self.title

    def getData(self):
        data = "Title: " + self.title + "\n" + "Description: " + self.description + "\n" + "Tags: " + \
            str(list(self.tags.values('title'))) + "\n"+"Pics: " + \
            str(list(self.pics.values('title'))) + "\n"+"AttachedFiles: " + \
            str(list(self.attachedFiles.values('title')))
        return data


class Valoration(models.Model):
    score = models.IntegerField(verbose_name=_("score"), validators=[
                                MinValueValidator(0), MaxValueValidator(5)])
    thread = models.ForeignKey(
        Thread, on_delete=models.CASCADE, verbose_name=_("thread"))
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, verbose_name=_("business"))

    class Meta:
        unique_together = (("thread", "business"),)


class Response(models.Model):
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, verbose_name=_("business"))
    thread = models.ForeignKey(
        Thread, on_delete=models.CASCADE, verbose_name=_("thread"))
    title = models.TextField(
        max_length=100, blank=False, verbose_name=_("title"))
    description = models.TextField(blank=False, verbose_name=_("description"))
    pics = models.ManyToManyField(URL, verbose_name=_("pics"))

    def __str__(self):
        return self.title

    def getData(self):
        data = "Thread: " + str(self.thread) + "\n"+"Title: " + self.title + \
            "\n"+"Description: " + self.description + \
            "\n"+"Pics: " + str(list(self.pics.values('title')))
        return data


class Challenge(models.Model):
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, verbose_name=_("business"))
    title = models.TextField(
        max_length=100, blank=False, verbose_name=_("title"))
    description = models.TextField(blank=False, verbose_name=_("description"))
    objectives = models.TextField(blank=False, verbose_name=_("objectives"))
    freelancers = models.ManyToManyField(
        Freelancer, verbose_name=_("freelancers"))

    def getData(self):
        data = "Title: " + self.title + "\n" + "Description: " + self.description + \
            "\n"+"Objectives: " + self.objectives + "\n" + \
            "Freelancers: " + str(list(self.freelancers.values("profile__name", "profile__surname"))) + "\n"
        return data

class ChallengeResponse(models.Model):
    freelancer = models.ForeignKey(
        Freelancer, on_delete=models.CASCADE, verbose_name=_("freelancer"))
    challenge = models.ForeignKey(
        Challenge, on_delete=models.CASCADE, verbose_name=_("challenge"))
    title = models.TextField(
        max_length=100, blank=False, verbose_name=_("title"))
    description = models.TextField(blank=False, verbose_name=_("description"))

    def __str__(self):
        return self.title

    def getData(self):
        data = "Challenge: " + str(self.challenge) + "\n"+"Title: " + self.title + "\n"+"Description: " + self.description
        return data


# Manager objects


class Event(models.Model):
    manager = models.ForeignKey(
        Manager, on_delete=models.CASCADE, verbose_name=_("manager"))
    location = models.TextField(blank=False, verbose_name=_("location"))
    title = models.TextField(max_length=150, blank=False,
                             verbose_name=_("title"))
    description = models.TextField(blank=False, verbose_name=_("description"))
    moment = models.DateTimeField(null=False)
    freelancers = models.ManyToManyField(
        Freelancer, verbose_name=_("freelancers"))
    companies = models.ManyToManyField(Business, verbose_name=_("companies"))

# Objects for all users


class Chat(models.Model):
    user1 = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name=_("user"), related_name="user1")
    user2 = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name=_("user"), related_name="user2")


class Message(models.Model):
    chat = models.ForeignKey(
        Chat, on_delete=models.CASCADE, verbose_name=_("chat"))
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("user"))
    text = models.TextField(blank=False)


def getCurriculumData(self):
    professionalExperiences = ProfessionalExperience.objects.filter(
        curriculum=self)
    formations = Formation.objects.filter(curriculum=self)
    graphicEngineExperiences = GraphicEngineExperience.objects.filter(
        curriculum=self)
    html5Showcase = HTML5Showcase.objects.get(curriculum=self)
    aptitudes = Aptitude.objects.filter(curriculum=self)
    links = Link.objects.filter(curriculum=self)

    data = "-----CURRICULUM-----\n\n"
    data = data + "-----FORMATIONS-----\n\n"
    for formation in list(formations):
        data = data + "\n" + formation.getData()

    data = data + "\n\n-----GRAPHIC ENGINE EXPERIENCES-----\n\n"
    for graphicEngineExperience in list(graphicEngineExperiences):
        data = data + "\n" + graphicEngineExperience.getData()

    data = data + "\n\n-----PROFESSIONAL EXPERIENCES-----\n\n"
    for professionalExperience in list(professionalExperiences):
        data = data + "\n" + professionalExperience.getData()

    data = data + "\n\n-----APTITUDES-----\n\n"
    for aptitude in list(aptitudes):
        data = data + "\n" + aptitude.getData()

    data = data + "\n\n-----LINKS-----\n\n"
    for link in list(links):
        data = data + "\n" + link.getData()

    data = data + "\n\n-----HTML5 SHOWCASE-----\n\n"

    data = data + html5Showcase.getData()

    return data


Curriculum.getData = getCurriculumData


def getFreelancerData(self):
    profile = self.profile
    data = "-----PROFILE-----\n\n"
    data = data + "Name: " + profile.name + "\n" + "Surname: " + profile.surname + "\n" + "Email: " + profile.email + "\n" + "City: " + profile.city + "\n" + "Postal code: " + profile.postalCode + "\n" + \
        "ID Card Number: " + profile.idCardNumber + "\n" + "Date of birth: " + profile.dateOfBirth.strftime(
            '%m/%d/%Y') + "\n" + "Phone number: " + profile.phoneNumber + "\n" + "Photo: " + profile.photo
    curriculum = Curriculum.objects.get(freelancer=self)
    data = data + "\n\n\n" + curriculum.getData()
    return data


Freelancer.getData = getFreelancerData


def getBusinessData(self):
    profile = self.profile
    data = "-----PROFILE-----\n\n"
    data = data + "Name: " + profile.name + "\n" + "Surname: " + profile.surname + "\n" + "Email: " + profile.email + "\n" + "City: " + profile.city + "\n" + "Postal code: " + profile.postalCode + "\n" + \
        "ID Card Number: " + profile.idCardNumber + "\n" + "Date of birth: " + profile.dateOfBirth.strftime(
            '%m/%d/%Y') + "\n" + "Phone number: " + profile.phoneNumber + "\n" + "Photo: " + profile.photo

    job_offers = JobOffer.objects.filter(business=self)
    threads = Thread.objects.filter(business=self)
    responses = Response.objects.filter(business=self)
    challenges = Challenge.objects.filter(business=self)

    data = data + "\n\n-----JOB OFFERS-----\n\n"
    for job_offer in list(job_offers):
        data = data + "\n" + job_offer.getData()

    data = data + "\n\n-----THREADS-----\n\n"
    for thread in list(threads):
        data = data + "\n" + thread.getData()

    data = data + "\n\n-----RESPONSES-----\n\n"
    for response in list(responses):
        data = data + "\n" + response.getData()

    data = data + "\n\n-----CHALLENGES-----\n\n"
    for challenge in list(challenges):
        data = data + "\n" + challenge.getData()

    return data


Business.getData = getBusinessData
