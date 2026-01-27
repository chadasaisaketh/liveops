from django.urls import path
from .views import login, register

urlpatterns = [
    path("auth/login/", login),
    path("auth/register/", register),
]
