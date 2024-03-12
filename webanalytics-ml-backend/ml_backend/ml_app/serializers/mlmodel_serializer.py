from rest_framework import serializers
from ..models import MLModel

import json

class MLModelSerializer(serializers.ModelSerializer):
    history = serializers.SerializerMethodField()

    def get_history(self, obj):
        if obj.history is None:
            return None 
        return json.loads(obj.history.replace("'", "\""))

    class Meta:
        model = MLModel
        fields = ['id', 'dataset', 'name', 'status','created_at', 'algorithm', 'task', 
                  'file_extension', 'input_shape', 'output_shape',  
                  'hidden_layers', 'features', 'target', 
                  'epochs', 'batch_size', 'timesteps', 'default_model', 'activation', 
                  'optimizer', 'num_trees', 'max_depth', 'last_trained','training_time', 'history']