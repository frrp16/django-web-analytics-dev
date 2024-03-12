import requests
import dotenv
import traceback

from django.conf import settings

from ..models import DatabaseConnection

def create_connection(connection: DatabaseConnection):
    try:
        data = {
                "id": str(connection.id),
                "database_type": connection.database_type,
                "host": connection.host,
                "port": connection.port,
                "database": connection.database,
                "username": connection.username,
                "password": connection.password,
                "ssl": connection.ssl
            }
        print(data)
        response = requests.post(
        f"{settings.ETL_BACKEND_URL}/connections/",
            json=data
        )
        # check for response status
        response.raise_for_status()
        return response.json()    
            
    except Exception as e:        
        # traceback.print_last()
        raise Exception(e)




