from django.forms import ModelForm, forms, CharField, Textarea, ModelMultipleChoiceField, TextInput, MultipleChoiceField,EmailField, ModelMultipleChoiceField,CheckboxSelectMultiple, DateField, DateInput,SelectDateWidget
from django.contrib.auth.forms import UserCreationForm
from AIM_GAMES.models import *
from django.contrib.auth.models import User, Group
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


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
            raise forms.ValidationError("Profile not valid")

    def save(self, commit=False):
        print('save: BusinessForm')
        obj = super(BusinessForm, self).save(commit=commit)
        obj.profile = self.profile_form.save()
        group = Group.objects.get(name='Business')
        obj.profile.user.groups.add(group)
        obj.save()
        return obj


class FreelancerForm(ModelForm):
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

    def clean(self):
        print('clean: FreelancerForm')
        if not self.profile_form.is_valid():
            raise forms.ValidationError("Profile not valid")

    def save(self, commit=False):
        print('save: FreelancerForm')
        obj = super(FreelancerForm, self).save(commit=commit)
        obj.profile = self.profile_form.save()
        group = Group.objects.get(name='Freelancer')
        obj.profile.user.groups.add(group)
        obj.save()
        return obj


class ProfileForm(ModelForm):
    # dateOfBirth = DateField(widget=SelectDateWidget)

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

    def clean(self):
        print('clean: ProfileForm')
        if not self.user_form.is_valid():
            raise forms.ValidationError("User not valid")

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
    title = CharField(widget=TextInput(), label='Title')
    description = CharField(widget=Textarea(), label='Description',)
    tags = ModelMultipleChoiceField(queryset=Tag.objects.all(), label='Tags', required=False,)
    images = CharField(widget=Textarea(), required=False, label='Images URL',)
    files = CharField(widget=Textarea(), required=False, label='Files URL',)

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
