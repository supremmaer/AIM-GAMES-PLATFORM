from django import forms
from django.contrib.auth import authenticate


class SignupForm(forms.Form):
    # TODO
    user = forms.CharField(label='Your user', max_length=100)


class LoginForm(forms.Form):
    # TODO
    user = forms.CharField(max_length=100, required=True, error_messages={'required': 'Please enter your username'})
    password = forms.CharField(max_length=100, required=True, error_messages={'required': 'Please enter your password'})

    def clean(self):
        # First, clean the form
        cleaned_data = super().clean()

        user = cleaned_data.get("user")
        password = cleaned_data.get("password")

        if user and password:
            # Only do something if both fields are valid so far.
            user = authenticate(username=cleaned_data.get('user'), password=cleaned_data.get('password'))
            if user is None:
                raise forms.ValidationError("Invalid username or password")

