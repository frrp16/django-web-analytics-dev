from .consumer import NotificationConsumer
from django.urls import include, path, re_path
from channels.generic.websocket import AsyncWebsocketConsumer

from channels.routing import ProtocolTypeRouter, URLRouter



websocket_urlpatterns = [
    # Create path for notification
    re_path(r'ws/notification/(?P<user_id>\w+)/$', NotificationConsumer.as_asgi()),
] 