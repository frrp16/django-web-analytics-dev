from ..models import DatabaseConnection
from rest_framework import serializers

class DatabaseConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatabaseConnection 
        fields = '__all__'