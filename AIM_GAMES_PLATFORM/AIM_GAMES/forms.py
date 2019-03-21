from django.forms import ModelForm, forms
from AIM_GAMES.models import Freelancer, Business, Profile


class FreelancerForm(ModelForm):
    # TODO Lógica
    class Meta:
        model = Freelancer
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(FreelancerForm, self).__init__(*args, **kwargs)
        self.fields['profile'].required = False
        data = kwargs.get('data')
        # 'prefix' parameter required if in a modelFormset
        self.profile_form = ProfileForm(instance=self.instance and self.instance.profile, prefix=self.prefix, data=data)

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
    # TODO Lógica
    class Meta:
        model = Profile
        exclude = ()
