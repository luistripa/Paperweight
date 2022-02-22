from typing import Union

from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpRequest


class LoginForm(forms.Form):
    username = forms.CharField(label='Username:', required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

    def login(self, request: HttpRequest) -> Union[User, None]:
        user: User = authenticate(username=self.cleaned_data["username"], password=self.cleaned_data["password"])
        if user is not None:
            login(request=request, user=user)
            return user
        return None
