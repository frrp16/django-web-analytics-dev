from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import MLModelViewSet

router = DefaultRouter()
router.register(r'mlmodel', MLModelViewSet, basename='MLModel')

app_urls = [
    path('', include(router.urls)),    
]
