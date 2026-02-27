# Created on 20260224 Tue by Guanglin Du.
# How to use django.contrib.auth.forms.UserCreationForm? - qianwen
# The django.contrib.auth.forms.UserCreationForm is a built-in Django form
# that handles user registration — including username, password, and
# password confirmation — with built-in validation and secure password
# handling.
from typing import TypeAlias
from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import User


class SignupForm(UserCreationForm):
    class Meta:
        model: TypeAlias = User
        fields: tuple[str, ...] = ('email', 'name', 'password1', 'password2')


class ProfileForm(forms.ModelForm):
    class Meta:
        model: TypeAlias = User
        fields: tuple[str, ...] = ('email', 'name', 'avatar',)
