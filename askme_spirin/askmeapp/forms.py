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
        try:
            models.User.objects.get(username=self.cleaned_data['username'])
        except:
            try:
                models.User.objects.get(email=self.cleaned_data['email'])
            except:
                return self.cleaned_data
            raise ValidationError('Email already taken')
        raise ValidationError('Username already taken')


class ProfileRegistrationForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ['avatar']
        ##widgets = {
        #    'avatar': forms.FileInput(label='Upload avatar', attrs={'class' : "col-4 login-field"})
        #}
