from rest_framework import serializers
from ..models import Dataset

        
class DatasetSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Dataset
        fields = '__all__'        

class CreateDatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ['name', 'description','table_name', 'user'] 
        extra_kwargs = {'user': {'write_only': True}}

