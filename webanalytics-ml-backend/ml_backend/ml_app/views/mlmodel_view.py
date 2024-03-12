# from ..tasks import train_model

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from ..models import MLModel
from ..serializers import MLModelSerializer

from ..services.dataset_service import get_dataset_data, update_training_status, get_dataset_instance

import pandas as pd
from pandas.api.types import is_bool_dtype
import numpy as np
import ast
import json
import uuid

from ..tasks import train_model 

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
    
    def create(self, request):
        try:
            serializer = MLModelSerializer(data=request.data)
            if serializer.is_valid():
                model_instance = serializer.save()                
                models = model_instance.build_and_compile_model()
                model_instance.save_model(models)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            traceback.print_exc() 
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, pk=None):
        try:
            model_instance = MLModel.objects.get(id=pk)
            serializer = MLModelSerializer(model_instance, data=request.data, partial=True)
            if serializer.is_valid():
                model_instance = serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            model_instance = MLModel.objects.get(id=pk)
            model_instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST) 
    
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
            model = MLModel.objects.get(id=str(request.data.get('model')))
            # print(request.data)
            # map request.data.get('features') from [{'column': col, 'type': type}] to [col1, col2, col3]
            features = list(map(lambda x: x['column'], request.data.get('features')))
            target = list(map(lambda x: x['column'], request.data.get('target')))
            sample_size = request.data.get('sample_size')
            sample_frac = request.data.get('sample_frac')
            scaler = request.data.get('scaler')

            model.features = features
            model.target = target
            model.sample_size = sample_size if sample_size != '' else None 
            model.sample_frac = sample_frac
            model.scaler = scaler

            model.save()
            # print(model.features)
            # print(model.target)
            # start training model
            train_model.delay(model.id)            
            
            return Response("Training started", status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'], url_path='history')
    def get_model_loss_history(self, request, pk=None):
        try:
            model = MLModel.objects.get(id=pk)
            history = model.history
            return Response(json.loads(history.replace("'", "\"")), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    
    @action(detail=True, methods=['GET'], url_path='summary')
    def get_model_summary(self, request, pk=None):
        try:
            model = MLModel.objects.get(id=pk)
            model_summary = model.get_model_summary()
            return Response(model_summary, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['POST'], url_path='predict')
    def predict(self, request, pk=None):
        try:
            model = MLModel.objects.get(id=pk)
            data = request.data.get('data')
            df_pred = pd.DataFrame(json.loads(data))
            # filter only features from models features
            features_list = ast.literal_eval(model.features)
            target_list = ast.literal_eval(model.target)
            # check if target are in dataset
            df_pred_target = None
            for col in target_list:
                if col in df_pred.columns:
                    df_pred_target = df_pred[col]

            # check if features are in the dataset
            for col in features_list:
                if col not in df_pred.columns:
                    raise Exception(f"Column {col} not in dataset")
            
            df_pred = df_pred[features_list]   

            # encode object columns
            for col in df_pred.columns:
                if df_pred[col].dtype == 'object':
                    df_pred[col] = df_pred[col].astype('category').cat.codes
            
            # encode boolean columns
            for col in df_pred.columns:
                if is_bool_dtype(df_pred[col]):
                    df_pred[col] = df_pred[col].astype(int)

            df_pred = df_pred.values.astype(np.float32)
            print(df_pred.shape)
            print(type(df_pred_target)) 
            # if algorithm is LSTM, reshape data
            if model.algorithm == 'LSTM':
                df_pred, _ = model.lstm_data_transform(df_pred, df_pred)
                print(df_pred.shape)
 
            # make prediction
            prediction = model.predict(df_pred)
            mse = None
            # if model is anomaly detection, calculate mse
            if model.task == 'Anomaly Detection':
                mse = np.mean(np.square(df_pred.values - prediction))
            
            # if df_pred_target is not None, add it to the response
            if df_pred_target is not None and model.algorithm != "RANDOM_FOREST":
                mse = np.mean(np.square(df_pred_target.values - prediction))

            response = {
                'prediction': prediction,
                'mse': mse if mse is not None else None
            }

            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        
        
    # @action(detail=True, methods=['GET'], url_path='layers')
    # def get_model_layers(self, request, pk=None):
    #     try:
    #         model = MLModel.objects.get(id=pk)
    #         layers = model.get_model_layers()
    #         return Response(layers, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        
    # @action(detail=True, methods=['POST'], url_path='predict')
    # def predict(self, request):  
    #     dataset_id = request.data.get('dataset_id')
    #     model_id = request.data.get('model_id')
    #     data_predict = request.data.get('data')

    #     try:
    #         model = MLModel.objects.get(id=model_id)
    #         df_predict = pd.DataFrame(data_predict)[model.features.split(',')]

    #         data_predict = pd.DataFrame(data_predict)
    #         prediction = model.predict(data_predict)
    #         return Response(prediction, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        
