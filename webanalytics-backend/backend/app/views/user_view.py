from rest_framework import permissions, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..services import register_user, logout_user, get_user_serialize
from ..serializers import UserSerializer

class RegisterView(APIView):
    serializers_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        response, status = register_user(request)
        return Response(response, status=status)

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