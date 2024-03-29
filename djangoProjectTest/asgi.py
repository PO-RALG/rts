"""
ASGI config for djangoProjectTest project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application


# application = get_asgi_application()

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.layers import get_channel_layer
from notifier import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProjectTest.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})

channel_layer = get_channel_layer()

