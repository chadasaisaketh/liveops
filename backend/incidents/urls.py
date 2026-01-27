from django.urls import path
from .views import incidents_view, resolve_incident

urlpatterns = [
    path("incidents/", incidents_view),
    path("incidents/<int:id>/resolve/", resolve_incident),
]
