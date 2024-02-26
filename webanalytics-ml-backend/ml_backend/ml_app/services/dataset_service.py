import requests
import pandas as pd
from django.conf import settings

import sqlalchemy

BACKEND_HOST = settings.BACKEND_HOST

def get_connection_url(connection_id, access_token):
    try:
        response = requests.get(f'http://{BACKEND_HOST}/connection/{connection_id}/url', headers={'Authorization': f'Bearer {access_token}'})        
        return response.json()
    except Exception as e:
        raise Exception(e)
def get_dataset_instance(dataset_id, access_token):
    try:
        response = requests.get(f'http://{BACKEND_HOST}/dataset/{dataset_id}', headers={'Authorization': f'Bearer {access_token}'})        
        return response.json()
    except Exception as e:
        raise Exception(e)

def get_dataset_columns(dataset_id, access_token):
    try:
        response = requests.get(f'http://{BACKEND_HOST}/dataset/{dataset_id}/columns', headers={'Authorization': f'Bearer {access_token}'})        
        return response.json()
    except Exception as e:
        raise Exception(e)
    
def get_dataset_data(connection_id, dataset_id, access_token) -> pd.DataFrame:
    try:
        connection_url = get_connection_url(connection_id, access_token)
        dataset_instance = get_dataset_instance(dataset_id, access_token)
        table_name = dataset_instance['table_name']
                
        engine = sqlalchemy.create_engine(connection_url)

        data = pd.read_sql(table_name, con=engine)                
        return data.to_dict(orient='records')

    except Exception as e:
        raise Exception(e)

def update_training_status(dataset_id, status, access_token):
    try:
        response = requests.patch(f'http://{BACKEND_HOST}/dataset/{dataset_id}/', 
                                  headers={'Authorization': f'Bearer {access_token}'}, 
                                  json={'is_trained': status}
                                  )
        return response.json()
    except Exception as e:
        raise Exception(e)
    
    
