from django import forms
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'col-7 login-field', 'placeholder': 'Username'}))
    password = forms.CharField(min_length=4, max_length=255, widget=forms.PasswordInput(
        attrs={'class': 'col-7 login-field', 'placeholder': 'Password'}))
