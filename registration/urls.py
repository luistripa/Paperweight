from django.contrib.auth.views import LoginView
from django.urls import path

from registration.views import logout_view

app_name = 'registration'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]

