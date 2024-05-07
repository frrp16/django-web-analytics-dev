from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RegisterView, LogoutView, UserView, LoginView
from .views import DatasetViewSet
from .views import TrainingView
# from .views import MLModelViewSet
from .views import DatabaseConnectionViewSet
from .views import NotificationViewSet
from .views import MLModelView

# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi
# from rest_framework import permissions

# schema_view = get_schema_view(
#     openapi.Info(
#         title="REST APIs",
#         default_version='v1'
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )

router = DefaultRouter()
router.register(r'users', UserView, basename='User')
router.register(r'connection', DatabaseConnectionViewSet, basename='DatabaseConnection')
router.register(r'dataset', DatasetViewSet, basename='Dataset')
router.register(r'notification', NotificationViewSet, basename='Notification')
router.register(r'mlmodel', MLModelView, basename='MLModel')

app_urls = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),   
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),    
]