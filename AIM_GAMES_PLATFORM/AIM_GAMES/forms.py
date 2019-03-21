from django.forms import ModelForm, forms, CharField, EmailField
from django.contrib.auth.forms import UserCreationForm
from AIM_GAMES.models import Freelancer, Business, Profile
from django.contrib.auth.models import User


class BusinessForm(ModelForm):
    # TODO Testear salvado
    class Meta:
        model = Business
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(BusinessForm, self).__init__(*args, **kwargs)
        self.fields['profile'].required = False
        data = kwargs.get('data')
        # 'prefix' parameter required if in a modelFormset
        self.profile_form = ProfileForm(instance=self.instance, prefix=self.prefix, data=data)

    def clean(self):
        if not self.profile_form.is_valid():
            raise forms.ValidationError(self.profile_form.errors)

    def save(self, commit=True):
        obj = super(BusinessForm, self).save(commit=commit)
        obj.profile = self.profile_form.save()
        return obj.save()


class FreelancerForm(ModelForm):
    # TODO Testear salvado
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
        obj.save()
        return obj


class ProfileForm(ModelForm):
    # TODO Testear salvado
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
    # TODO Testear salvado

    class Meta:
        model = User
        fields = ['username']

    # def __init__(self, *args, **kwargs):
    #     print('__init__ UserForm')
    #     super(UserForm, self).__init__(*args, **kwargs)

    # def save(self, commit=False):
    #     print('save: UserForm')
    #     obj = super(UserForm, self).save(commit=commit)
    #     return obj


