from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from ..models import DatasetMonitorLog

from ..serializers import DatasetMonitorLogSerializer

from ..tasks import monitor_single_dataset

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
    
    def create(self, request):
        serializer = DatasetMonitorLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # get monitor logs for a dataset
    @action(detail=False, methods=['GET'], url_path='dataset/(?P<dataset_id>[^/.]+)')
    def get_monitor_logs(self, request, dataset_id):
        queryset = DatasetMonitorLog.objects.filter(dataset=dataset_id)
        serializer = DatasetMonitorLogSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['POST'], url_path='monitor')
    def monitor_dataset(self, request):
        try:
            dataset_id = request.data.get('dataset_id')
            if not dataset_id:
                return Response("Invalid data", status=status.HTTP_400_BAD_REQUEST)
            monitor_single_dataset.delay(dataset_id)
            return Response("Monitoring task started", status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
