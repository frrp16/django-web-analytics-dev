from .tasks import train_model

from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import MLModel
from .serializers import MLModelSerializer
from .services.dataset_service import get_dataset_data, update_training_status

import pandas as pd
import ast


class MLModelViewSet(viewsets.ViewSet):    
    serializer_class = MLModelSerializer

    # def list(self, request):
    #     queryset = MLModel.objects.all()
    #     serializer = mlmodel.MLModelSerializer(queryset, many=True)
    #     return Response(serializer.data)
    def list(self, request):
        queryset = MLModel.objects.all()
        serializer = MLModelSerializer(queryset, many=True)
        return Response(serializer.data) 

    
    def retrieve(self, request, pk=None):        
        queryset = MLModel.objects.get(id=pk)       
        serializer = MLModelSerializer(queryset)        
        return Response(serializer.data)
    
    @action(detail=False, methods=['POST'], url_path='train')
    def train_model(self, request):        
        try:
            access_token = request.headers.get('Authorization').split(' ')[1]
            connection_id = request.data.get('connection_id')
            dataset_id = request.data.get('dataset_id')
            features = request.data.get('features')
            target = request.data.get('target')
            algorithm = request.data.get('algorithm')
            task = request.data.get('task')
            hidden_layers = request.data.get('hidden_layers')
            epochs = request.data.get('epochs')
            batch_size = request.data.get('batch_size')            

            if not all([connection_id, dataset_id]):
                return Response("Invalid data", status=status.HTTP_400_BAD_REQUEST)
                        
            # Get dataset data
            data_json = get_dataset_data(connection_id, dataset_id, access_token)
            
            # print(type(features))
            # print(type(target))
            # print(type(hidden_layers))
            
            features = ast.literal_eval(features)
            target = ast.literal_eval(target)                                
            hidden_layers = ast.literal_eval(hidden_layers)

            # print(type(features))
            # print(type(target))
            # print(type(hidden_layers))

            # Convert epoch and batch_size to int
            epochs = int(epochs)
            batch_size = int(batch_size)

            # Convert data to pandas dataframe
            # data = pd.DataFrame(data_json)

            # if not all([features, target, algorithm, task, hidden_layers]):
            #     return Response("Invalid data", status=status.HTTP_400_BAD_REQUEST)

            # start training model
            train_model.delay(
                name='model_name',
                dataset=data_json,
                features=features,
                target=target,
                scaler=None,
                algorithm=algorithm,
                task=task,
                hidden_layers=hidden_layers,
                dataset_id=dataset_id,
                epochs=epochs,
                batch_size=batch_size,
                access_token=access_token
            )
            # update training status
            update_training_status(dataset_id, 'TRAINING', access_token)
            return Response("Training started", status=status.HTTP_200_OK)
        except Exception as e:
            update_training_status(dataset_id, 'UNTRAINED', access_token)
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
    
    # def create(self, request):
    #     name = request.data.get('name')
    #     algorithm = request.data.get('algorithm')
    #     workspace = request.data.get('workspace')
    #     files = request.data.get('files')

    #     # Validate the data
    #     if not all([name, algorithm, workspace, files]):
    #         return Response("Invalid data", status=status.HTTP_400_BAD_REQUEST)
        
    #     # Get file instance from files that contains files_id
    #     files_instance = Files.objects.get(id=files)
    #     # Get Workspace instance from workspace that contains workspace_id
    #     workspace_instance = Workspace.objects.get(id=workspace)

    #     # Create a new MLModel instance
    #     model_instance = MLModel(name=name, algorithm=algorithm, workspace=workspace_instance, files=files_instance)

    #     # Save the MLModel instance
    #     model_instance.save()
    #     serializer = mlmodel.MLModelSerializer(model_instance)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['GET'], url_path='summary')
    def get_model_summary(self, request, pk=None):
        try:
            model = MLModel.objects.get(id=pk)
            model_summary = model.get_model_summary()
            return Response(model_summary, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)