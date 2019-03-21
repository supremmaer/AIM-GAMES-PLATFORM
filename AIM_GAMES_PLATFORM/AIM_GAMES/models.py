from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.contrib.auth.hashers import make_password

# Create your models here.
# System objects


class Tag(models.Model):
    title = models.TextField(max_length=20, primary_key=True, blank=False)
    def __str__(self):
        return self.title


class GraphicEngine(models.Model):
    title = models.TextField(max_length=50, primary_key=True, blank=False)
    def __str__(self):
        return self.title


# Misc


class URL(models.Model):
    title = models.URLField()
    def __str__(self):
        return self.title


# Profile class. Attributes regarding all users of the system go here


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.TextField(max_length=30, blank=False)
    surname = models.TextField(max_length=50, blank=False)
    email = models.EmailField(blank=False)
    city = models.TextField(max_length=30, blank=False)
    postalCode = models.TextField(max_length=16, blank=False)
    idCardNumber = models.TextField(max_length=10, blank=False)
    dateOfBirth = models.DateTimeField(null=False)
    phoneNumber = models.TextField(max_length=20, blank=False)
    photo = models.URLField()
    def __str__(self):
        return self.name


# Types of users


class Freelancer(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    profession = models.TextField(max_length=100)
    def __str__(self):
        return self.profile.email

    def get_absolute_url(self):
        return reverse('signupFreelancer', kwargs={'pk': self.pk})

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password


class Business(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    def __str__(self):
        return self.profile.email

# Freelancer objects


class ProfessionalExperience(models.Model):
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    center = models.TextField(max_length=50, blank=False)
    formation = models.TextField(max_length=100, blank=False)
    startDate = models.DateTimeField(null=False)
    endDate = models.DateTimeField(null=False)
    miniature = models.URLField()


class Formation(models.Model):
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    center = models.TextField(max_length=50, blank=False)
    formation = models.TextField(max_length=100, blank=False)
    startDate = models.DateTimeField(null=False)
    endDate = models.DateTimeField(null=False)
    miniature = models.URLField()


class GraphicEngineExperience(models.Model):
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    graphicEngine = models.ManyToManyField(
        GraphicEngine)
    graphicExperience = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)])


class HTML5Showcase(models.Model):
    freelancer = models.OneToOneField(Freelancer, on_delete=models.CASCADE)
    embedCode = models.TextField()


class Aptitude(models.Model):
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    aptitude = models.TextField(max_length=30, blank=False)


class Link(models.Model):
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    url = models.URLField(blank=False)

# Business objects


class JobOffer(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    position = models.TextField(max_length=100, blank=False)
    experienceRequired = models.TextField(max_length=100, blank=False)
    schedule = models.TextField(max_length=100, blank=False)
    salary = models.IntegerField(null=False)
    ubication = models.TextField(max_length=100, blank=False)
    description = models.TextField(max_length=10000, blank=False)
    images = models.TextField(blank=False)


class Valoration(models.Model):
    score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)])


class Thread(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    valoration = models.ForeignKey(Valoration, on_delete=models.CASCADE)
    title = models.TextField(max_length=100, blank=False)
    description = models.TextField(blank=False)
    tags = models.ManyToManyField(Tag)
    pics = models.ManyToManyField(URL, related_name="pic")
    attachedFiles = models.ManyToManyField(URL, related_name="attachedFile")
    def __str__(self):
        return self.title

class Response(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    title = models.TextField(max_length=100, blank=False)
    description = models.TextField(blank=False)
    pics = models.ManyToManyField(URL)
    def __str__(self):
        return self.title
