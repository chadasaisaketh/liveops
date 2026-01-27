from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path("admin/", admin.site.urls),

    # Auth
    path("api/auth/", include("accounts.urls")),
    path("api/auth/refresh/", TokenRefreshView.as_view()), 

    # Incidents
    path("api/", include("incidents.urls")),
]
