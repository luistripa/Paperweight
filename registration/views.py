from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import redirect


# Create your views here.

@login_required
def logout_view(request: HttpRequest, *args, **kwargs):
    logout(request)
    return redirect('/index')
