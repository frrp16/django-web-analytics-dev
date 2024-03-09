from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from django.utils import timezone

from ..models import DatasetTable, DatabaseConnection
from ..serializers import DatasetTableSerializer

from ..tasks import load_data_task

class DatasetTableViewSet(viewsets.ViewSet):
    
    serializer_class = DatasetTableSerializer
    # permission_classes = [permissions.IsAuthenticated]    

    def list(self, request):
        queryset = DatasetTable.objects.all()
        serializer = DatasetTableSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        queryset = DatasetTable.objects.get(pk=pk)
        serializer = DatasetTableSerializer(queryset)
        return Response(serializer.data)
    
    def create(self, request):
        id = request.data['id']        
        connection = request.data['connection']
        table_name = request.data['table_name']
        try:
            if id is None  or connection is None or table_name is None:
                return Response('Invalid request', status=status.HTTP_400_BAD_REQUEST) 

            connection_instance = DatabaseConnection.objects.get(id=connection)

            dataset_table = DatasetTable(
                id=id, connection=connection_instance, table_name=table_name
            )        
            dataset_table.save()
            load_data_task.delay(dataset_table.id)        
            serializer = DatasetTableSerializer(dataset_table)        
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)  
        except Exception as e:  
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)      
        
    @action(detail=False, methods=['POST'], url_path='load')
    def load(self, request):
        try:
            dataset_table_id = request.data['dataset_table_id']                        
            load_data_task.delay(dataset_table_id)
            return Response('Loading data...', status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['POST'], url_path='refresh')
    def refresh(self, request):
        try:
            dataset_table_id = request.data['dataset_table_id']            
            dataset_instace = DatasetTable.objects.get(id=dataset_table_id)                           
            if dataset_instace.date_updated > timezone.now() - timezone.timedelta(minutes=5):
                return Response(
                    f"Dataset {dataset_instace.table_name} was updated less than 5 minutes ago. Skipping...", 
                    status=status.HTTP_200_OK)
            load_data_task.delay(dataset_table_id)
            return Response('Refreshing data...', status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)