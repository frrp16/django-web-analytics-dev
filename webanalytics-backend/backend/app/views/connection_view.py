from django.contrib.auth.models import User

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import BasicAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from ..models import DatabaseConnection
from ..serializers import DatabaseConnectionSerializer
from ..services import user_service


class DatabaseConnectionViewSet(viewsets.ViewSet):
    ppermission_classes = [permissions.IsAuthenticated | permissions.IsAdminUser]    
    authentication_classes = [JWTAuthentication, BasicAuthentication]
    serializer_class = DatabaseConnectionSerializer

    def list(self, request):
        user = user_service.get_user_from_token(request.headers.get('Authorization').split()[1])
        queryset = DatabaseConnection.objects.filter(user=user)
        serializer = DatabaseConnectionSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        queryset = DatabaseConnection.objects.get(id=pk)
        serializer = DatabaseConnectionSerializer(queryset)
        return Response(serializer.data)
        
    def create(self, request):
        database_type = request.data['database_type']
        host = request.data['host']
        port = request.data['port']
        database = request.data['database']
        username = request.data['username']
        password = request.data['password']
        ssl = request.data['ssl']

        # Get user id
        user_id = 0
        token = request.headers.get('Authorization').split()[1]
        try:
            user_id = AccessToken(token).get('user_id')
            if not user_id:
                return Response("User not found or token is not valid", status=400)
        except Exception as e:
            return Response(str(e), status=400)
        
        user_instance = User.objects.get(id=user_id)
        db_instance = DatabaseConnection(
            user=user_instance, database_type=database_type, host=host, port=port, database=database, 
            username=username, password=password, ssl=ssl
        )

        # test connection
        try:
            db_instance.connect()
            db_instance.save()
            serializer = DatabaseConnectionSerializer(db_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(str(e), status=400)
        
    @action(detail=True, methods=['GET'], url_path='url')
    def get_connection_url(self, request, pk=None):
        try:
            if request.user.is_staff:
                db_instance = DatabaseConnection.objects.get(id=pk)
                url = db_instance.get_connection_url()
                return Response(url, status=200)
            else:
                return Response("Unauthorized", status=401)
        except Exception as e:
            return Response(str(e), status=400)

        