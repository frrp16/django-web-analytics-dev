from rest_framework import serializers
from ..models import MLModel

class MLModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLModel
        fields = ['id','name', 'algorithm', 'created_at', 'file_extension', 'features','target', 'dataset']