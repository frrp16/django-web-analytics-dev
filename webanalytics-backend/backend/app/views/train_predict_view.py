from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response

from ..services import user_service
from ..models import DatabaseConnection

from django.conf import settings

import requests
import traceback
import json

class TrainingView(APIView):
    def post(self, request):
        """
        Train a model with the given dataset
        request body:
        {
            dataset_id: int,
            algorithm: string,
            name: string,            
            features: [string, string, ...],
            target: [string],
            scaler: string, # minmax, standard, none
            hidden_layers: [int, int, ...], # only for 'MLP' algorithm
            epochs: int, # optional, default is 100
            batch_size: int, # optional, default is 32,
            timesteps: int, # only for 'LSTM' algorithm, optional, default is 5
        }
        """
        try: 
            user = user_service.get_user_from_token(request.headers.get('Authorization').split()[1])
            data = request.data
            if (type(data) != dict):
                data = data.dict()
            queryset = DatabaseConnection.objects.filter(user=user.id)
            print(data)

            data['connection_id'] = queryset[0].id
            data['epochs'] = 100 if 'epochs' not in data else data['epochs']
            data['batch_size'] = 32 if 'batch_size' not in data else data['batch_size']
            data['timesteps'] = 5 if 'timesteps' not in data else data['timesteps']

            url = f"{settings.ML_BACKEND_URL}/mlmodel/train/"
            response = requests.post(url, data=data)
            return Response(response.json(), status=response.status_code)
        except Exception as e:            
            traceback.print_exc()
            return Response(str(e), status=500)
        