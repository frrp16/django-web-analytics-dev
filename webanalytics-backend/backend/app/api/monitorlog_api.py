from django.conf import settings

import requests

def create_monitorlog(dataset_id, row_count, column_count):
    response = requests.post(
        f"{settings.ML_BACKEND_URL}/monitorlog/",
        json={
            "dataset": dataset_id,
            "row_count": row_count,
            "column_count": column_count
        }
    )
    response.raise_for_status()
    return response.json()

def get_dataset_monitorlog(dataset_id):
    response = requests.get(f"{settings.ML_BACKEND_URL}/monitorlog/dataset/{dataset_id}")
    response.raise_for_status()
    return response.json()