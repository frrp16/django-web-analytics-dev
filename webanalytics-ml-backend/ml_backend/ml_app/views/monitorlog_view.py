from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from ..models import DatasetMonitorLog

from ..serializers import DatasetMonitorLogSerializer

class MonitorLogViewSet(viewsets.ViewSet):
    serializer_class = DatasetMonitorLogSerializer

    def list(self, request):
        queryset = DatasetMonitorLog.objects.all()
        serializer = DatasetMonitorLogSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = DatasetMonitorLog.objects.get(id=pk)
        serializer = DatasetMonitorLogSerializer(queryset)
        return Response(serializer.data)
    
    # get monitor logs for a dataset
    @action(detail=False, methods=['GET'], url_path='dataset/(?P<dataset_id>[^/.]+)')
    def get_monitor_logs(self, request, dataset_id):
        queryset = DatasetMonitorLog.objects.filter(dataset=dataset_id)
        serializer = DatasetMonitorLogSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = DatasetMonitorLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
