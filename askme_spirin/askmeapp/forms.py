from django import forms
from django.core.exceptions import ValidationError
from askmeapp import models


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'col-7 login-field', 'placeholder': 'Username'}))
    password = forms.CharField(min_length=4, max_length=255, widget=forms.PasswordInput(
        attrs={'class': 'col-7 login-field', 'placeholder': 'Password'}))


class RegistrationForm(forms.ModelForm):
    repeat_password = forms.CharField(max_length=255, label='Repeat password', widget=forms.PasswordInput(
        attrs={'class': 'col-7 login-field', 'placeholder': 'Repeat password'}))

    class Meta:
        model = models.User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'col-7 login-field', 'placeholder': 'Username'}),
            'password': forms.PasswordInput(
                attrs={'class': 'col-7 login-field', 'placeholder': 'Password'}),
            'email': forms.EmailInput(
                attrs={'class': 'col-7 login-field', 'placeholder': 'Email'})
        }

    def clean(self):
        password1 = self.cleaned_data['password']
        password2 = self.cleaned_data['repeat_password']

        if password1 != password2:
            raise ValidationError("Passwords do not match", code='fail repeat')
        return self.cleaned_data

    def clean_username(self):
        try:
            models.User.objects.get(username=self.cleaned_data['username'])
        except:
            return self.cleaned_data['username']
        raise ValidationError('Username already taken')

    def clean_email(self):
        try:
            models.User.objects.get(email=self.cleaned_data['email'])
        except:
            return self.cleaned_data['email']
        raise ValidationError('Email already taken')

    def save(self):
        return models.User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'])


class ProfileRegistrationForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ['avatar']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'id': 'choose-file'})
        }
