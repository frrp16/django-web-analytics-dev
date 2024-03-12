from django.conf import settings

import json
import requests

def create_model(data):
    try:
        url = f"{settings.ML_BACKEND_URL}/mlmodel/"
        response = requests.post(url, json=data)
        return response.json()
    except Exception as e:
        raise Exception(e)
    
def get_model_by_id(id):
    try:
        url = f"{settings.ML_BACKEND_URL}/mlmodel/{id}/"
        response = requests.get(url)
        return response.json()
    except Exception as e:
        raise Exception(e)

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
    
def get_model_loss_history(model_id):
    try:
        url = f"{settings.ML_BACKEND_URL}/mlmodel/{model_id}/history/"
        response = requests.get(url)
        return response.json()
    except Exception as e:
        raise Exception(e)

def update_model(model_id, data):
    try:
        url = f"{settings.ML_BACKEND_URL}/mlmodel/{model_id}/"
        response = requests.patch(url, json=data)
        return response.json()
    except Exception as e:
        raise Exception(e)
    
def train_model(data):
    try:
        url = f"{settings.ML_BACKEND_URL}/mlmodel/train/"
        response = requests.post(url, json=data)
        return response.json()
    except Exception as e:
        raise Exception(e)