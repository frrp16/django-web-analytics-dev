from rest_framework import permissions, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from django.conf import settings

import requests

class TrainingView(APIView):
    def post(self, request):
        try: 
            url = f"{settings.ML_BACKEND_URL}/train/"
            data = request.data
            response = requests.post(url, data=data)
            return Response(response.json(), status=response.status_code)
        except Exception as e:
            return Response(str(e), status=500)