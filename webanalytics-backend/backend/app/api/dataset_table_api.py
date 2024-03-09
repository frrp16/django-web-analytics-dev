import requests

from django.conf import settings
from ..models import Dataset

def create_dataset_table(dataset: Dataset):
    try:
        response = requests.post(
        f"{settings.ETL_BACKEND_URL}/tables/", 
            json={
                "id": str(dataset.id),                
                "connection": str(dataset.connection.id),
                "table_name": dataset.table_name,
            }   
        )
        # check for response status
        response.raise_for_status()
        return response.json()    
            
    except Exception as e:        
        # traceback.print_last()
        raise Exception(e)

def refresh_dataset_table(dataset_id):
    try:
        response = requests.post(
        f"{settings.ETL_BACKEND_URL}/tables/refresh/", 
            json={
                "dataset_table_id": dataset_id
            }   
        )
        # check for response status
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise Exception(e) 