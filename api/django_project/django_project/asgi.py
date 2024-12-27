"""
ASGI config for django_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from opentelemetry.instrumentation.asgi import OpenTelemetryMiddleware

from .urls import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")

application = OpenTelemetryMiddleware(
    ProtocolTypeRouter(
        {
            "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
        }
    )
)
