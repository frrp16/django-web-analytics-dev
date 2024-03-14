from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import BasicAuthentication

from ..services import user_service
from ..models import DatabaseConnection

from ..api import get_model_by_dataset_id, get_model_summary
from ..api import create_model, train_model, get_model_by_id, get_model_loss_history, update_model


from django.conf import settings

import requests
import traceback
import json


class MLModelView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated | permissions.IsAdminUser]
    authentication_classes = [JWTAuthentication, BasicAuthentication]

    def list(self, request):        
        return(Response("MLModelView", status=200))

    def retrieve(self, request, pk=None):
        """
        Get model summary by model id
        """
        try:
            response = get_model_by_id(pk)
            return Response(response, status=200)
        except Exception as e:
            return Response(str(e), status=500)

    def create(self, request):
        """
        Create model
        """
        try:
            data = request.data 
            # if dataset_id is not exist
            if not data.get('dataset'):
                return Response("Dataset id is required", status=400)

            response = create_model(data)
            return Response(response, status=200)
        except Exception as e:
            return Response(str(e), status=500)

    def destroy(self, request, pk=None):
        """
        Delete model
        """
        try:
            url = f"{settings.ML_BACKEND_URL}/mlmodel/{pk}/"
            response = requests.delete(url)
            return Response(response, status=200) 
        except Exception as e:
            return Response(str(e), status=500)

    @action(detail=False, methods=['get'], url_path='dataset/(?P<dataset_id>[^/.]+)')
    def get_model_by_dataset_id(self, request, dataset_id=None):        
        """
        Get model by dataset id
        """
        try:
            response = get_model_by_dataset_id(dataset_id)
            return Response(response, status=200)
        except Exception as e:
            return Response(str(e), status=500)
        
    @action(detail=True, methods=['GET'], url_path='history')
    def get_model_loss_history(self, request, pk=None):
        """
        Get model loss history by model id
        """
        try:
            response = get_model_loss_history(pk)
            return Response(response, status=200)
        except Exception as e: 
            return Response(str(e), status=500)
        
    @action(detail=True, methods=['GET'], url_path='summary')
    def get_model_summary(self, request, pk=None):
        """
        Get model summary by model id
        """
        try:
            response = get_model_summary(pk)
            return Response(response, status=200)
        except Exception as e:
            return Response(str(e), status=500)
    
    @action(detail=True, methods=["PATCH"], url_path='update')
    def update_model(self, request, pk=None):
        """
        Update model
        """
        try:
            data = request.data
            response = update_model(pk, data)
            return Response(response, status=200)
        except Exception as e:
            return Response(str(e), status=500)
    
    

    @action(detail=False, methods=['post'], url_path='train')
    def train_model(self, request):
        """
        Train model
        """
        try:
            data = request.data
            print(data)
            response = train_model(data)
            return Response(response, status=200)
        except Exception as e:
            return Response(str(e), status=500)
        
    @action(detail=True, methods=['POST'], url_path='predict')
    def predict(self, request, pk=None):
        """
        Predict
        """
        try:
            data = request.data
            response = requests.post(
                f"{settings.ML_BACKEND_URL}/mlmodel/{pk}/predict/",
                json=data
            )
            response.raise_for_status()
            return Response(response.json(), status=200)
        except Exception as e:
            return Response(str(e), status=500)

    @action(detail=True, methods=['DELETE'], url_path='prediction/(?P<prediction_id>[^/.]+)/delete')
    def delete_prediction_history(self, request, pk=None, prediction_id=None):
        """
        Delete prediction history
        """
        try:
            url = f"{settings.ML_BACKEND_URL}/prediction/{prediction_id}/"
            response = requests.delete(url)
            return Response(response, status=200)
        except Exception as e:
            return Response(str(e), status=500)
    
    