from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(label='Search Word', max_length=100)

# forms.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']