from ..models import DatasetTable
from rest_framework import serializers        
        
class DatasetTableSerializer(serializers.ModelSerializer):  
    # monitor_log = DatasetMonitorLogSerializer(many=True, read_only=True)  
    class Meta:
        model = DatasetTable
        fields = '__all__'
