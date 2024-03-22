from rest_framework import serializers
from ..models import MLModel, PredictionModel


import json 

class PredictionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredictionModel
        fields = ['id', 'model', 'created_at','loss','prediction']

class MLModelSerializer(serializers.ModelSerializer):
    features = serializers.SerializerMethodField() 
    target = serializers.SerializerMethodField()
    history = serializers.SerializerMethodField()
    prediction = serializers.SerializerMethodField()
    
    def get_features(self, obj): 
        if obj.features is None:
            return None
        # check if obj.features has "" quotes
        if obj.features.find("\"") != -1:
            return json.loads(obj.features)
        return json.loads(obj.features.replace("'", "\""))
    
    def get_target(self, obj):
        if obj.target is None:
            return None
        # check if obj.target has "" quotes
        if obj.target.find("\"") != -1:
            return json.loads(obj.target)
        return json.loads(obj.target.replace("'", "\"")) 
    

    
    def get_history(self, obj):
        if obj.history is None:
            return None 
        return json.loads(obj.history.replace("'", "\""))
    
    def get_prediction(self, obj):  
        return PredictionModel.objects.filter(model=obj.id).values()

    class Meta:
        model = MLModel
        fields = ['id', 'dataset', 'name', 'status','created_at', 'algorithm', 'task', 
                  'file_extension', 'input_shape', 'output_shape',  
                  'hidden_layers', 'features', 'target', 
                  'epochs', 'batch_size', 'timesteps', 'default_model', 'activation', 
                  'optimizer', 'num_trees', 'max_depth', 'last_trained','training_time', 'history', 'prediction']


