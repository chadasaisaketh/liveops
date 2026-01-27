import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "liveops.settings")

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

from incidents.middleware import JWTAuthMiddleware


django_asgi_app = get_asgi_application()

import incidents.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": JWTAuthMiddleware(
        URLRouter(
            incidents.routing.websocket_urlpatterns
        )
    ),
})
