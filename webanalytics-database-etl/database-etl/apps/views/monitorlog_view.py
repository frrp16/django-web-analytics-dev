from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from ..models import DatasetMonitorLog
from ..serializers import DatasetMonitorLogSerializer


        
class DatasetMonitorLogViewSet(viewsets.ViewSet):
    serializer_class = DatasetMonitorLogSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        queryset = DatasetMonitorLog.objects.all()
        serializer = DatasetMonitorLogSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        queryset = DatasetMonitorLog.objects.get(pk=pk)
        serializer = DatasetMonitorLogSerializer(queryset)
        return Response(serializer.data)
    
    # get monitor logs for a dataset
    @action(detail=False, methods=['GET'], url_path='dataset/(?P<dataset_id>[^/.]+)')
    def get_dataset_monitorlog(self, request, dataset_id):
        queryset = DatasetMonitorLog.objects.filter(dataset_table=dataset_id)
        serializer = DatasetMonitorLogSerializer(queryset, many=True)
        return Response(serializer.data)