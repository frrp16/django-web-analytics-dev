from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import BasicAuthentication
from rest_framework_simplejwt.tokens import AccessToken

from ..models import Notification
from ..serializers import NotificationSerializer

from ..services import get_user_from_token

class NotificationViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated | permissions.IsAdminUser]    
    authentication_classes = [JWTAuthentication, BasicAuthentication]
    serializer_class = NotificationSerializer

    def list(self, request):
        try:
            if request.user.is_staff:
                notifications = Notification.objects.all()
                serializer = NotificationSerializer(notifications, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            user = get_user_from_token(request.headers.get('Authorization').split()[1])
            notifications = Notification.objects.filter(user=user)
            serializer = NotificationSerializer(notifications, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def create(self, request):
        try:
            serializer = NotificationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)