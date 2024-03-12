import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
from django.conf import settings

import os
import dotenv
from sqlalchemy import create_engine, URL, text

dotenv.load_dotenv()

database_etl_url = URL.create(
    drivername='postgresql',
    username=os.getenv('WAREHOUSE_DATABASE_USER'),
    password=os.getenv('WAREHOUSE_DATABASE_PASSWORD'),
    host=os.getenv('WAREHOUSE_DATABASE_HOST'),
    port=os.getenv('WAREHOUSE_DATABASE_PORT'),
    database=os.getenv('WAREHOUSE_DATABASE_NAME')
)

database_etl_engine = create_engine(database_etl_url)

BACKEND_HOST = settings.BACKEND_HOST

def get_connection_instance(connection_id):
    try:
        response = requests.get(f'{BACKEND_HOST}/connection/{connection_id}', 
                                auth=HTTPBasicAuth(os.environ.get('API_USER'), os.environ.get('API_PASSWORD')))       
        return response.json()
    except Exception as e:
        raise Exception(e)

def get_dataset_instance(dataset_id):
    try:
        response = requests.get(f'{BACKEND_HOST}/dataset/{dataset_id}', 
                                auth=HTTPBasicAuth(os.environ.get('API_USER'), os.environ.get('API_PASSWORD')))        
        return response.json()
    except Exception as e:
        raise Exception(e)

def get_dataset_columns(dataset_id):
    try:
        response = requests.get(f'{BACKEND_HOST}/dataset/{dataset_id}/columns', 
                                auth=HTTPBasicAuth(os.environ.get('API_USER'), os.environ.get('API_PASSWORD')))        
        return response.json()
    except Exception as e:
        raise Exception(e)

def get_dataset_row_count(dataset_id):
    try:
        response = requests.get(f'{BACKEND_HOST}/dataset/{dataset_id}/row_count', 
                                auth=HTTPBasicAuth(os.environ.get('API_USER'), os.environ.get('API_PASSWORD')))        
        return response.json()
    except Exception as e:
        raise Exception(e)
    
def get_dataset_data(dataset_id) -> pd.DataFrame:   
    try:
        dataset_instance = get_dataset_instance(dataset_id)
        connecion_instance = get_connection_instance(dataset_instance['connection'])
        table_name = f"{connecion_instance['database']}_{dataset_instance['table_name']}"

        data = pd.read_sql(table_name, con=database_etl_engine)                
        return data.to_dict(orient='records')

    except Exception as e:
        raise Exception(e)

def update_training_status(dataset_id, status):
    try:
        response = requests.patch(f'{BACKEND_HOST}/dataset/{dataset_id}/', 
                                  auth=HTTPBasicAuth(os.environ.get('API_USER'), os.environ.get('API_PASSWORD')), 
                                  json={'is_trained': status}
                                  )
        return response.json()
    except Exception as e:
        raise Exception(e)

def update_dataset_change_status(dataset_id, status):
    try: 
        response = requests.patch(f'{BACKEND_HOST}/dataset/{dataset_id}/', 
                                  auth=HTTPBasicAuth(os.environ.get('API_USER'), os.environ.get('API_PASSWORD')), 
                                  json={'status': status}
                                  ) 
        return response.json()
    except Exception as e:
        raise Exception(e)

# def update_monitor_log(dataset_id, row_count, column_count, access_token):
#     try:
#         response = requests.post(f'{BACKEND_HOST}/dataset/{dataset_id}/monitor_log', 
#                                   headers={'Authorization': f'Bearer {access_token}'}, 
#                                   json={'row_count': row_count, 'column_count': column_count}
#                                   )
#         return response.json()
#     except Exception as e:
#         raise Exception(e)
    
