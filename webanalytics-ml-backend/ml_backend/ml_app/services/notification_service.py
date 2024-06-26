import requests
import os
from requests.auth import HTTPBasicAuth
from django.conf import settings

from dotenv import load_dotenv

load_dotenv()

def create_notification(title, user, message, type, context):
    try:
        response = requests.post(f'{settings.BACKEND_HOST}/notification/', 
                                json={'title': title, 'user': user, 'message': message, 'type': type, 'context': context},
                               auth=HTTPBasicAuth(os.getenv('API_USER'), os.getenv('API_PASSWORD')))        
        return response.json()
    except Exception as e:
        raise Exception(e)