from django.urls import path
from .views import list_incidents

urlpatterns = [
    path("incidents/", list_incidents),
]
