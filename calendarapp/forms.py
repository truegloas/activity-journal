from django import forms
from .models import *
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in (self.fields['email'], self.fields['password1'], self.fields['password2']):
            field.widget.attrs.update({'class': 'form-control'})


class UserAuthenticationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password')
        widgets = {
                   'email': forms.TextInput(attrs={'class': 'form-control'}),
                   'password': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserAuthenticationForm, self).__init__(*args, **kwargs)
        for field in (self.fields['email'], self.fields['password']):
            field.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        if self.is_valid():

            email = self.cleaned_data.get('email')
            password = self.cleaned_data.get('password')
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Ошибка авторизации')


class UserUpdatePassword(PasswordChangeForm):
    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')
        widgets = {
            'old_password': forms.TextInput(attrs={'class': 'form-control'}),
            'new_password1': forms.TextInput(attrs={'class': 'form-control'}),
            'new_password2': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserUpdatePassword, self).__init__(*args, **kwargs)
        for field in (self.fields['old_password'], self.fields['new_password1'], self.fields['new_password2']):
            field.widget.attrs.update({'class': 'form-control'})
