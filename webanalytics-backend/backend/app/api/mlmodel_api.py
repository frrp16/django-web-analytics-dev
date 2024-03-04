from django.conf import settings

import requests


def get_model_by_dataset_id(dataset_id):
    try:
        url = f"{settings.ML_BACKEND_URL}/mlmodel/dataset"
        response = requests.get(url, params={'dataset': dataset_id})
        return response.json()
    except Exception as e:
        raise Exception(e)
    
def get_model_summary(model_id):
    try:
        url = f"{settings.ML_BACKEND_URL}/mlmodel/{model_id}/summary/"
        response = requests.get(url)
        return response.json()
    except Exception as e:
        raise Exception(e)