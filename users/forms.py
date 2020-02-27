from django import forms
from django.contrib.auth.models import User as Users
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = Users
        fields = ['username', 'email', 'password1', 'password2']
