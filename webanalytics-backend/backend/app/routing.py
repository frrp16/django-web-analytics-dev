from .routes import analysis_url

from .consumer import NotificationConsumer
from django.urls import include, path, re_path

from channels.routing import ProtocolTypeRouter, URLRouter

websocket_urlpatterns = [
    # path(r'ws/', URLRouter(preprocesssing_url)),
    # path(r'ws/', URLRouter(analysis_url)),    
    # Create path for notification
    re_path(r'ws/notification/(?P<user_id>\w+)/$', NotificationConsumer.as_asgi()), 
    # path(r'ws/', URLRouter(training_url)),
] 