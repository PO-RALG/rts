from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from notifier.consumers import NotificationConsumer
from . import views

application = ProtocolTypeRouter({
    'websocket': URLRouter([
        path('ws/notifications/', NotificationConsumer.as_asgi()),
    ]),
})

urlpatterns = [
    path('send_notification/', views.send_notification, name='send_notification'),
]
