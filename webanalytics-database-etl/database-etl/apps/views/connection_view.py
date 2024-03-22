from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from django.utils import timezone
import traceback

from ..models import DatabaseConnection
from ..serializers import DatabaseConnectionSerializer

class DatabaseConnectionViewSet(viewsets.ViewSet):
    def list(self, request):        
        queryset = DatabaseConnection.objects.all()
        serializer = DatabaseConnectionSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        queryset = DatabaseConnection.objects.get(id=pk)
        serializer = DatabaseConnectionSerializer(queryset)
        return Response(serializer.data)
        
    def partial_update(self, request, pk=None):
        instance = DatabaseConnection.objects.get(id=pk)
        serializer = DatabaseConnectionSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        id = request.data['id']
        database_type = request.data['database_type']
        host = request.data['host']
        port = request.data['port']
        database = request.data['database']
        username = request.data['username']
        password = request.data['password']
        ssl = request.data['ssl']      

        # print(request.data) 

        if id is None or database_type is None or host is None or port is None or database is None or username is None or password is None:
            return Response('Invalid request', status=status.HTTP_400_BAD_REQUEST)
                
        db_instance = DatabaseConnection(
            id=id,
            database_type=database_type, host=host, port=port, database=database, 
            username=username, password=password, ssl=ssl
        )
        # test connection
        try:
            db_instance.connect()
            db_instance.save()
            serializer = DatabaseConnectionSerializer(db_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            traceback.print_exc()
            return Response(str(e), status=400)