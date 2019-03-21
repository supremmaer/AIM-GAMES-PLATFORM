from django.forms import ModelForm, forms, CharField, EmailField
from django.contrib.auth.forms import UserCreationForm
from AIM_GAMES.models import Freelancer, Business, Profile
from django.contrib.auth.models import User


class FreelancerForm(ModelForm):
    # TODO Testear salvado
    class Meta:
        model = Freelancer
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(FreelancerForm, self).__init__(*args, **kwargs)
        self.fields['profile'].required = False
        data = kwargs.get('data')
        # 'prefix' parameter required if in a modelFormset
        self.profile_form = ProfileForm(instance=self.instance, prefix=self.prefix, data=data)

    def clean(self):
        if not self.profile_form.is_valid():
            raise forms.ValidationError("Profile not valid")

    def save(self, commit=True):
        obj = super(FreelancerForm, self).save(commit=commit)
        obj.profile = self.profile_form.save()
        obj.save()



class BusinessForm(forms.Form):
    # TODO Lógica
    class Meta:
        model = Business
        exclude = ()


class ProfileForm(ModelForm):
    # TODO Testear salvado
    class Meta:
        model = Profile
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['user'].required = True
        data = kwargs.get('data')
        # 'prefix' parameter required if in a modelFormset
        self.user_form = UserForm(instance=self.instance, prefix=self.prefix, data=data)

    def clean(self):
        if not self.user_form.is_valid():
            raise forms.ValidationError("User not valid")

    def save(self, commit=True):
        obj = super(ProfileForm, self).save(commit=commit)
        obj.user = self.user_form.save()
        obj.save()


class UserForm(UserCreationForm):
    # TODO Testear salvado

    class Meta:
        model = User
        fields = ['username']
