from django.urls import path, include

from .views import DatabaseConnectionViewSet, DatasetTableViewSet, DatasetMonitorLogViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'tables', DatasetTableViewSet, basename='dataset-tables')
router.register(r'connections', DatabaseConnectionViewSet, basename='database-connections')
router.register(r'logs', DatasetMonitorLogViewSet, basename='dataset-monitor-logs')

app_urls = [
    path('', include(router.urls)),
]

