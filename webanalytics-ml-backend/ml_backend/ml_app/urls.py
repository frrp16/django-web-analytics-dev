from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import MLModelViewSet, PredictionModelViewSet

router = DefaultRouter()
router.register(r'mlmodel', MLModelViewSet, basename='MLModel')
router.register(r'prediction', PredictionModelViewSet, basename='PredictionModel')

app_urls = [
    path('', include(router.urls)),    
]
