from rest_framework import serializers
from ..models import DatabaseConnection

class DatabaseConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatabaseConnection
        fields = '__all__'
        
        extra_kwargs = {'password': {'write_only': True}, 'user': {'write_only': True}} 