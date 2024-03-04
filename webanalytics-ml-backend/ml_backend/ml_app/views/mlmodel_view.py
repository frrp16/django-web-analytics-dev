from ..tasks import train_model

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from ..models import MLModel
from ..serializers import MLModelSerializer

from ..services.dataset_service import get_dataset_data, update_training_status, get_dataset_instance

import pandas as pd
import ast
import uuid

import traceback

class MLModelViewSet(viewsets.ViewSet):    
    serializer_class = MLModelSerializer

    def list(self, request):
        queryset = MLModel.objects.all()
        serializer = MLModelSerializer(queryset, many=True)
        return Response(serializer.data) 
    
    def retrieve(self, request, pk=None):        
        queryset = MLModel.objects.get(id=pk)       
        serializer = MLModelSerializer(queryset)        
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'], url_path='dataset')
    def get_model_by_dataset(self, request):
        dataset_id = request.query_params.get('dataset')
        try:
            queryset = MLModel.objects.filter(dataset=dataset_id)
            serializer = MLModelSerializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
             
    @action(detail=False, methods=['POST'], url_path='train')
    def train_model(self, request):        
        try:     
            name = request.data.get('name')       
            connection_id = request.data.get('connection_id')
            dataset_id = request.data.get('dataset_id')
            features = request.data.getlist('features')
            target = request.data.getlist('target')            
            algorithm = request.data.get('algorithm')
            task = request.data.get('task')
            # optional
            scaler = request.data.get('scaler')  # standard, minmax
            hidden_layers = request.data.getlist('hidden_layers')
            epochs = request.data.get('epochs')
            batch_size = request.data.get('batch_size')             
            timesteps = request.data.get('timesteps')


            print(f"Features: {features}")
            print(f"Target: {target}")
            print(f"Hidden layers: {hidden_layers}")

            if not all([connection_id, dataset_id]):
                return Response("Invalid data", status=status.HTTP_400_BAD_REQUEST)
                        
            # Get dataset data
            data_json = get_dataset_data(connection_id, dataset_id)
            dataset_instance_json = get_dataset_instance(dataset_id)

            # if data_json have more than 50000 data, sample
            if len(data_json) > 50000:
                print("Sampling data")
                df = pd.DataFrame(data_json)
                data_json = df.sample(n=50000).to_dict(orient='records')
            
            # if type(features) == str:
            #     features = ast.literal_eval(features)
            # if type(target) == str:
            #     target = ast.literal_eval(target)

            # convert ['1', '2', '3'] to [1, 2, 3]
            hidden_layers = list(map(int, hidden_layers))

            # Convert epoch and batch_size to int
            epochs = int(epochs)
            batch_size = int(batch_size)

            # start training model
            train_model.delay(
                name=name,
                dataset=data_json,
                features=features,
                target=target,
                scaler=scaler,
                algorithm=algorithm,
                task=task,
                hidden_layers=hidden_layers,
                dataset_id=dataset_id,
                epochs=epochs,
                batch_size=batch_size,
                timesteps=timesteps,
                user_id=dataset_instance_json['user']
                                
            )
            # update training status
            update_training_status(dataset_id, 'TRAINING')
            return Response("Training started", status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            update_training_status(dataset_id, 'UNTRAINED')
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['GET'], url_path='summary')
    def get_model_summary(self, request, pk=None):
        try:
            model = MLModel.objects.get(id=pk)
            model_summary = model.get_model_summary()
            return Response(model_summary, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)