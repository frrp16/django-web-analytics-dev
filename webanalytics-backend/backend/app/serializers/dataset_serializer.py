from rest_framework import serializers
from ..models import Dataset

        
class DatasetSerializer(serializers.ModelSerializer):   
    # add columns to the serializer
    columns = serializers.SerializerMethodField()
    def get_columns(self, obj):
        return obj.get_dataset_columns(use_cache=True)

    class Meta:
        model = Dataset
        fields = ['id', 'name', 'description', 'table_name', 'created_at', 'status', 'is_trained', 'columns', 'user', 'connection']

class CreateDatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ['name', 'description','table_name', 'user'] 
        extra_kwargs = {'user': {'write_only': True}}

