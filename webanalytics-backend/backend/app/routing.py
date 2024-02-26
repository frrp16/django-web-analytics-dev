from .routes import preprocesssing_url, analysis_url, training_url
from django.urls import include, path

from channels.routing import ProtocolTypeRouter, URLRouter

websocket_urlpatterns = [
    path(r'ws/', URLRouter(preprocesssing_url)),
    path(r'ws/', URLRouter(analysis_url)),
    path(r'ws/', URLRouter(training_url)),
] 