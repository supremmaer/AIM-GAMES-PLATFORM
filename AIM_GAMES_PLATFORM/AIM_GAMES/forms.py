from django.forms import ModelForm, forms, CharField,URLField, URLInput,Textarea,DateTimeField, ModelMultipleChoiceField,EmailInput, NumberInput, TextInput, MultipleChoiceField,EmailField, ModelMultipleChoiceField,CheckboxSelectMultiple, DateField, DateInput,SelectDateWidget,ChoiceField,RadioSelect
from django.contrib.auth.forms import UserCreationForm
from AIM_GAMES.models import *
from django.contrib.auth.models import User, Group
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from datetime import datetime,timedelta


class BusinessForm(ModelForm):
    class Meta:
        model = Business
        exclude = ('lastPayment',)

    def __init__(self, *args, **kwargs):
        super(BusinessForm, self).__init__(*args, **kwargs)
        self.fields['profile'].required = False
        data = kwargs.get('data')
        # 'prefix' parameter required if in a modelFormset
        self.instance.profile = Profile()
        self.profile_form = ProfileForm(instance=self.instance and self.instance.profile, prefix=self.prefix, data=data)

    def clean(self):
        if not self.profile_form.is_valid():
            raise forms.ValidationError(_("Profile not valid"))

    def save(self, commit=False):
        print('save: BusinessForm')
        obj = super(BusinessForm, self).save(commit=commit)
        obj.profile = self.profile_form.save()
        group = Group.objects.get(name='Business')
        obj.profile.user.groups.add(group)
        obj.save()
        return obj


class FreelancerForm(ModelForm):
    profession = CharField(widget=TextInput(), label=_("profession"))
    class Meta:
        model = Freelancer
        exclude = ()

    def __init__(self, *args, **kwargs):
        print('__init__ FreelancerForm')
        super(FreelancerForm, self).__init__(*args, **kwargs)
        self.fields['profile'].required = False
        data = kwargs.get('data')
        # 'prefix' parameter required if in a modelFormset
        self.instance.profile = Profile()
        self.profile_form = ProfileForm(instance=self.instance and self.instance.profile, prefix=self.prefix, data=data)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'validate'

    def clean(self):
        print('clean: FreelancerForm')
        if not self.profile_form.is_valid():
            raise forms.ValidationError(_("Profile not valid"))

    def save(self, commit=False):
        print('save: FreelancerForm')
        obj = super(FreelancerForm, self).save(commit=commit)
        obj.profile = self.profile_form.save()
        group = Group.objects.get(name='Freelancer')
        obj.profile.user.groups.add(group)
        obj.save()
        return obj


class ProfileForm(ModelForm):
    name = CharField(widget=TextInput(), label=_("Name"))
    surname = CharField(widget=TextInput(), label=_("Surname"))
    email = EmailField(widget=EmailInput(), label=_("Email"))
    city = CharField(widget=TextInput(), label=_("City"))
    postalCode = CharField(widget=NumberInput(), label=_("Postal Code"))
    idCardNumber = CharField(widget=TextInput(), label=_("IDCard Number"))
    dateOfBirth = DateField(widget=DateInput(), label=_("Date of birth"))
    phoneNumber = CharField(widget=NumberInput(), label=_("Phone Number"))
    photo = URLField(widget=URLInput(), label=_("Photo URL:"))

    class Meta:
        model = Profile
        exclude = ()

    def __init__(self, *args, **kwargs):
        print('__init__ ProfileForm')
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['user'].required = False
        data = kwargs.get('data')
        # 'prefix' parameter required if in a modelFormset
        self.instance.user = User()
        self.user_form = UserForm(instance=self.instance and self.instance.user, prefix=self.prefix, data=data)

    def clean_phoneNumber(self):
        print('clean: ProfileForm: PhoneNumber')
        data = self.cleaned_data['phoneNumber']
        if not data.isdigit():
            raise ValidationError(_("Phone Number must be a number"))
        return data

    def clean_dateOfBirth(self):
        print('clean: ProfileForm: dateOfBityh')
        data = self.cleaned_data['dateOfBirth']
        from_date = datetime.now() - timedelta(days=18*365)
        print(str(from_date))
        print(str(data))
        if data > datetime.date(from_date):
            raise ValidationError(_("You must be over 18 to sign up"))
        return data

    def clean(self):
        print('clean: ProfileForm')
        if not self.user_form.is_valid():
            raise forms.ValidationError(_("User not valid"))

    def save(self, commit=False):
        print('save: ProfileForm')
        obj = super(ProfileForm, self).save(commit=commit)
        obj.user = self.user_form.save()
        obj.save()
        return obj


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username']


class ThreadForm(ModelForm):
    title = CharField(widget=TextInput(), label=_('Title'))
    description = CharField(widget=Textarea(), label=_('Description'),)
    tags = ModelMultipleChoiceField(queryset=Tag.objects.all(), label=_('Tags'), required=False,)
    images = CharField(widget=Textarea(), required=False, label=_('Image URLs'),)
    files = CharField(widget=Textarea(), required=False, label=_('Attachment URLs'),)

    class Meta:
        model = Thread
        exclude = ('business', 'pics', 'attachedFiles')


    def clean_images(self):
        """Split the tags string on whitespace and return a list"""
        print('clean: ThreadForm: Images')
        return self.cleaned_data['images'].strip().split()

    def clean_files(self):
        """Split the tags string on whitespace and return a list"""
        print('clean: ThreadForm: Files')
        return self.cleaned_data['files'].strip().split()

    def __init__(self, *args, **kwargs):
        print('__init__ ThreadForm')
        super(ThreadForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'validate'


    def clean(self):
        print('clean: ThreadForm')
        val = URLValidator()
        urls = self.cleaned_data['images']
        try:
            for url in urls:
                val(url)

            urls = self.cleaned_data['files']
            for url in urls:
                val(url)
        except ValidationError:
            raise ValidationError("Please, enter valid URLS separated by comas in the images and files field")

    def save(self,business):
        print('save: ProfileForm')
        obj = super(ThreadForm, self).save(commit=False)
        pics = []
        attached_files = []
        for image in self.cleaned_data['images']:
            url = URL.objects.filter(title=image)
            if not url:
                url = URL()
                url.title = image
                url.save()
            else:
                url = url[0]
            pics.append(url)
        for file in self.cleaned_data['files']:
            url = URL.objects.filter(title=file)
            if not url:
                url = URL()
                url.title = file
                url.save()
            else:
                url = url[0]
            attached_files.append(url)

        obj.business = business[0]
        obj.save()
        obj.attachedFiles.set(attached_files)
        obj.pics.set(pics)
        return obj

class ResponseForm(ModelForm):

    class Meta:
        model = Response
        exclude = ('business','thread')

class LinkForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        print('__init__ LinkForm')
        super(LinkForm, self).__init__(*args, **kwargs)
        data = kwargs.get('data')
        print('xd')

    class Meta:
        model = Link
        exclude = ('curriculum',)

class GraphicEngineExperienceForm(ModelForm):

    class Meta:
        model = GraphicEngineExperience
        exclude = ['curriculum']

class AptitudeForm(ModelForm):

    class Meta:
        model = Aptitude
        exclude = ['curriculum']

class ProfessionalExperienceForm(ModelForm):
    """ startDate = DateField(widget=SelectDateWidget()) """
    class Meta:
        model = ProfessionalExperience
        exclude = ['curriculum']

class FormationForm(ModelForm):

    class Meta:
        model = Formation
        exclude = ['curriculum']

class html5showcaseForm(ModelForm):

    class Meta:
        model = HTML5Showcase
        exclude = ['curriculum']

class JobOfferForm(ModelForm):

    class Meta:
        model = JobOffer
        exclude = ['business']