from .routes import analysis_url

from .consumer import NotificationConsumer
from django.urls import include, path, re_path
from channels.generic.websocket import AsyncWebsocketConsumer

from channels.routing import ProtocolTypeRouter, URLRouter

class DemoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        await self.send(text_data=text_data)
    


websocket_urlpatterns = [
    # path(r'ws/', URLRouter(preprocesssing_url)),
    # path(r'ws/', URLRouter(analysis_url)),    
    # Create path for notification
    re_path(r'ws/notification/(?P<user_id>\w+)/$', NotificationConsumer.as_asgi()), 
    path(r'demo', DemoConsumer.as_asgi()),
    # path(r'ws/', URLRouter(training_url)),
] 