from rest_framework import permissions, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from ..services import register_user, logout_user, get_user_serialize, get_user_from_token
from ..serializers import UserSerializer

from django.contrib.auth.models import User

from ..models import Notification

class RegisterView(APIView):
    serializers_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        response, status = register_user(request)
        return Response(response, status=status)
    
class LoginView(TokenObtainPairView):
    # if login, create Notification
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = get_user_from_token(response.data['access'])
        notification = Notification(title="Login Success", user=user, message="Login Success", type="info", context="AUTH")
        notification.save()
        return response

class LogoutView(APIView):
    def post(self, request):
        response, status = logout_user(request)
        return Response(response, status=status)

class UserView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def list(self, request):
        response = get_user_serialize(request)
        return Response(response)