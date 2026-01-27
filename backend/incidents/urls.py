from django.urls import path
from .views import list_incidents, create_incident, resolve_incident

urlpatterns = [
    path("incidents/", list_incidents),
    path("incidents/create/", create_incident),
    path("incidents/<int:id>/resolve/", resolve_incident),
]
