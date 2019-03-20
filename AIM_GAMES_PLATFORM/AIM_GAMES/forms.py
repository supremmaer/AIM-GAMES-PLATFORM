from django import forms


class SignupForm(forms.Form):
    # TODO
    user = forms.CharField(label='Your user', max_length=100)


class LoginForm(forms.Form):
    # TODO
    user = forms.CharField(label='Username:', max_length=100, required=True, error_messages={'required': 'Please enter your username'})
    password = forms.CharField(label='Username:', max_length=100, required=True, error_messages={'required': 'Please enter your password'})
