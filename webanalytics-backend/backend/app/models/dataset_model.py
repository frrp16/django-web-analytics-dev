from django.db import models
from django.core.cache import cache
from django.contrib.auth.models import User

from .connection_model import DatabaseConnection

import uuid
import pandas as pd

from sqlalchemy import create_engine, URL, text

class Dataset(models.Model):
    class DatasetStatus(models.TextChoices):
        CHANGED = 'CHANGED'
        STABLE = 'STABLE'
    class DatasetTrainingStatus(models.TextChoices):
        TRAINING = 'TRAINING'
        TRAINED = 'TRAINED'
        UNTRAINED = 'UNTRAINED'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    table_name = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=7, choices=DatasetStatus.choices, default=DatasetStatus.STABLE)
    is_trained = models.CharField(max_length=9, choices=DatasetTrainingStatus.choices, default=DatasetTrainingStatus.UNTRAINED)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='datasets')
    connection = models.ForeignKey(DatabaseConnection, on_delete=models.CASCADE, null=True)

    def get_dataset_data(self):
        try:
            df = cache.get(f'dataset_{self.id}_data')
            if df is not None:
                return df
            else:
                print("Cache not found")
                engine = self.connection.engine_instance
                df = pd.read_sql_table(self.table_name, con=engine)
                cache.set(f'dataset_{self.id}_data', df)
                engine.dispose()
                return df 
        except Exception as e:
            raise Exception(e)
    
    def get_dataset_columns(self):
        try:            
            conn = self.connection.connect()
            query = text("SELECT column_name as column FROM information_schema.columns WHERE table_name = :x").bindparams(x=f"{self.table_name}")  
            cursor = conn.execute(query)
            conn.close()  
            self.connection.disconnect()       
            return [item['column'] for item in cursor.mappings().all()]
        except Exception as e:
            raise Exception(e)
        
    def get_dataset_row_count(self):
        try:
            engine = self.connection.engine_instance
            conn = engine.connect()
            query = text(f"SELECT COUNT(*) FROM {self.table_name}")
            cursor = conn.execute(query)
            conn.close()
            self.connection.disconnect()
            return cursor.scalar()
        except Exception as e:
            raise Exception(e)

    def __str__(self):
        return self.name