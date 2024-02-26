from django.contrib.auth.models import User
from rest_framework import serializers

from .dataset_serializer import DatasetSerializer
from .connection_serializer import DatabaseConnectionSerializer

class UserSerializer(serializers.ModelSerializer):
    connection = DatabaseConnectionSerializer(many=False, read_only=True)
    datasets = DatasetSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password','connection','datasets')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user