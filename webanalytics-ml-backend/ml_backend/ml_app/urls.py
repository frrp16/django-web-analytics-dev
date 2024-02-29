from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import MLModelViewSet, MonitorLogViewSet

router = DefaultRouter()
router.register(r'mlmodel', MLModelViewSet, basename='MLModel')
router.register(r'monitorlog', MonitorLogViewSet, basename='MonitorLog')

app_urls = [
    path('', include(router.urls)),    
]
