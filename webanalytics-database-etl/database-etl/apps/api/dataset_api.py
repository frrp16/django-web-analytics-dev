import requests
import os
from requests.auth import HTTPBasicAuth
from django.conf import settings

from dotenv import load_dotenv

load_dotenv()

def get_dataset_instance(dataset_id):
    try:
        response = requests.get(f'{settings.BACKEND_HOST}/dataset/{dataset_id}', 
                                auth=HTTPBasicAuth(os.environ.get('API_USER'), os.environ.get('API_PASSWORD')))        
        return response.json()
    except Exception as e:
        raise Exception(e)