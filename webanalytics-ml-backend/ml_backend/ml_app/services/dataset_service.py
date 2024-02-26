import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
from django.conf import settings

import sqlalchemy
import os

from dotenv import load_dotenv

load_dotenv()

BACKEND_HOST = settings.BACKEND_HOST

def get_connection_url(connection_id):
    try:
        response = requests.get(f'http://{BACKEND_HOST}/connection/{connection_id}/url', 
                                auth=HTTPBasicAuth(os.environ.get('API_USER'), os.environ.get('API_PASSWORD')))       
        return response.json()
    except Exception as e:
        raise Exception(e)

def get_dataset_instance(dataset_id):
    try:
        response = requests.get(f'http://{BACKEND_HOST}/dataset/{dataset_id}', 
                                auth=HTTPBasicAuth(os.environ.get('API_USER'), os.environ.get('API_PASSWORD')))        
        return response.json()
    except Exception as e:
        raise Exception(e)

def get_dataset_columns(dataset_id):
    try:
        response = requests.get(f'http://{BACKEND_HOST}/dataset/{dataset_id}/columns', 
                                auth=HTTPBasicAuth(os.environ.get('API_USER'), os.environ.get('API_PASSWORD')))        
        return response.json()
    except Exception as e:
        raise Exception(e)
    
def get_dataset_data(connection_id, dataset_id) -> pd.DataFrame:
    try:
        connection_url = get_connection_url(connection_id)
        dataset_instance = get_dataset_instance(dataset_id)
        table_name = dataset_instance['table_name']
                
        engine = sqlalchemy.create_engine(connection_url)

        data = pd.read_sql(table_name, con=engine)                
        return data.to_dict(orient='records')

    except Exception as e:
        raise Exception(e)

def update_training_status(dataset_id, status):
    try:
        response = requests.patch(f'http://{BACKEND_HOST}/dataset/{dataset_id}/', 
                                  auth=HTTPBasicAuth(os.environ.get('API_USER'), os.environ.get('API_PASSWORD')), 
                                  json={'is_trained': status}
                                  )
        return response.json()
    except Exception as e:
        raise Exception(e)

# def update_monitor_log(dataset_id, row_count, column_count, access_token):
#     try:
#         response = requests.post(f'http://{BACKEND_HOST}/dataset/{dataset_id}/monitor_log', 
#                                   headers={'Authorization': f'Bearer {access_token}'}, 
#                                   json={'row_count': row_count, 'column_count': column_count}
#                                   )
#         return response.json()
#     except Exception as e:
#         raise Exception(e)
    
