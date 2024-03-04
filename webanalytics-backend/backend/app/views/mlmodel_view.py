from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import BasicAuthentication

from ..services import user_service
from ..models import DatabaseConnection

from ..api import get_model_by_dataset_id, get_model_summary


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
            response = get_model_summary(pk)
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