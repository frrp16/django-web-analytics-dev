from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RegisterView, LogoutView, UserView
from .views import DatasetViewSet
# from .views import MLModelViewSet
from .views import DatabaseConnectionViewSet

from .views import PlotView

router = DefaultRouter()
router.register(r'users', UserView, basename='User')
router.register(r'connection', DatabaseConnectionViewSet, basename='DatabaseConnection')
router.register(r'dataset', DatasetViewSet, basename='Dataset')
# router.register(r'mlmodel', MLModelViewSet, basename='MLModel')
router.register(r'plot', PlotView, basename='Plot')

app_urls = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),    
    path('', include(router.urls)),    
]