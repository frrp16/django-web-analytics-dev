from django.db import models

import uuid
import pandas as pd
import dotenv
import os

from sqlalchemy import create_engine, URL
from .connection_model import DatabaseConnection

dotenv.load_dotenv()
# connection to database_etl
database_etl_url = URL.create(
    drivername='postgresql',
    username=os.getenv('DATABASE_USER'),
    password=os.getenv('DATABASE_PASSWORD'),
    host=os.getenv('DATABASE_HOST'),
    port=os.getenv('DATABASE_PORT'),
    database=os.getenv('DATABASE_NAME')
)

database_etl_engine = create_engine(database_etl_url)

class DatasetTable(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    connection = models.ForeignKey(DatabaseConnection, on_delete=models.CASCADE)
    date_updated = models.DateTimeField(auto_now=True)
    table_name = models.CharField(max_length=255)

    def extract_data(self):
        try:
            connection = self.connection.connect()
            result = pd.read_sql_table(self.table_name, connection)
            connection.close()
            return result
        except Exception as e:
            raise Exception(e)
        
    def load_data(self, data: pd.DataFrame):
        try:                  
            etl_conn = database_etl_engine.connect()
            data.to_sql(f"{self.connection.database}_{self.table_name}", etl_conn, if_exists='replace', index=False)            
            etl_conn.close()              
        except Exception as e:
            raise Exception(e)