from rest_framework import serializers
from ..models import Dataset
from ..api import get_model_by_dataset_id, get_dataset_monitorlog
        
class DatasetSerializer(serializers.ModelSerializer):   
    # add columns to the serializer
    columns = serializers.SerializerMethodField()
    models = serializers.SerializerMethodField()
    monitor_log = serializers.SerializerMethodField()
    
    def get_columns(self, obj):
        return obj.get_dataset_columns_type()
    def get_models(self, obj):
        try:
            return get_model_by_dataset_id(obj.id)            
        except Exception as e:
            return str(e)
    def get_monitor_log(self, obj):
        try:
            return get_dataset_monitorlog(obj.id)            
        except Exception as e:
            return str(e)

    class Meta:
        model = Dataset
        fields = ['id', 'name', 'description', 'table_name', 'created_at', 'status', 'is_trained', 'columns', 'user', 'connection', 'models', 'monitor_log']

class CreateDatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ['name', 'description','table_name', 'user'] 
        extra_kwargs = {'user': {'write_only': True}}

