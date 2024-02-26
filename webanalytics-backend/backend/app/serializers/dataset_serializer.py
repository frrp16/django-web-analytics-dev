from rest_framework import serializers
from ..models import Dataset, DatasetMonitorLog


class DatasetMonitorLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetMonitorLog
        fields = '__all__'
        extra_kwargs = {'dataset': {'write_only': True}}
        
class DatasetSerializer(serializers.ModelSerializer):
    monitor_logs = DatasetMonitorLogSerializer(many=True, read_only=True)
    class Meta:
        model = Dataset
        fields = '__all__'
        extra_kwargs = {'user': {'write_only': True}}

class CreateDatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ['name', 'description','table_name', 'user'] 
        extra_kwargs = {'user': {'write_only': True}}

