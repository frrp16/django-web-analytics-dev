from ..models import DatasetMonitorLog
from rest_framework import serializers

class DatasetMonitorLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetMonitorLog
        fields = ['id', 'date_updated', 'row_count', 'column_count', 'changes']
