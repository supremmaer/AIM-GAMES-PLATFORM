from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.utils.text import capfirst

import unicodedata

UserModel = get_user_model()


class SignupForm(forms.Form):
    # TODO
    user = forms.CharField(label='Your user', max_length=100)

