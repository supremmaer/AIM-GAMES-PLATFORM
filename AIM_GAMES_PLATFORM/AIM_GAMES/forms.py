from django.forms import ModelForm, forms, CharField, EmailField, ModelMultipleChoiceField,CheckboxSelectMultiple, DateField, DateInput,SelectDateWidget
from django.contrib.auth.forms import UserCreationForm
from AIM_GAMES.models import Freelancer, Business, Profile, Thread, Tag
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


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
    # Cada chip es un diccionario, tengo que mandar un array de diccionarios
    chips = CharField()

    class Meta:
        model = Thread
        exclude = ('business', 'valoration', 'tags', 'pics', 'attachedFiles')

    def __init__(self, *args, **kwargs):
        print('__init__ ThreadForm')
        # Only in case we build the form from an instance
        # (otherwise, 'tags' list should be empty)

        super(ThreadForm, self).__init__(*args, **kwargs)

    def clean(self):
        print('clean: ThreadForm')
        print(self.data )


