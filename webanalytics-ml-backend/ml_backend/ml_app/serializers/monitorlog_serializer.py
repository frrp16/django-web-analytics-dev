from rest_framework import serializers
from ..models import DatasetMonitorLog

class DatasetMonitorLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetMonitorLog
        fields = "__all__"