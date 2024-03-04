from django.db import models
from django.core.cache import cache
from django.contrib.auth.models import User

from .connection_model import DatabaseConnection

import uuid
import pandas as pd
import json 

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
                engine = self.connection.engine_instance
                df = pd.read_sql_table(self.table_name, con=engine)
                cache.set(f'dataset_{self.id}_data', df)
                engine.dispose()
                return df 
        except Exception as e:
            raise Exception(e)
    
    def get_dataset_columns(self, use_cache=False):
        try:            
            if use_cache:                
                columns = cache.get(f'dataset_{self.id}_columns')
                if columns is not None:
                    return columns   
            conn = self.connection.connect()
            query = text("SELECT column_name as column FROM information_schema.columns WHERE table_name = :x").bindparams(x=f"{self.table_name}")  
            cursor = conn.execute(query)
            conn.close()  
            self.connection.disconnect()     
            columns = [item['column'] for item in cursor.mappings().all()]
            cache.set(f'dataset_{self.id}_columns', columns)  
            return columns
        except Exception as e:
            raise Exception(e)
        
    def get_dataset_columns_type(self, use_cache=False):
        try:
            if use_cache:
                columns_type = cache.get(f'dataset_{self.id}_columns_type')
                if columns_type is not None:
                    return columns_type
            df = self.get_dataset_data()
            columns_type = df.dtypes.astype(str).to_dict()
            cache.set(f'dataset_{self.id}_columns_type', columns_type)             
            return columns_type
        except Exception as e:
            raise Exception(e) 
        
    def get_dataset_row_count(self, use_cache=False):
        try:
            if (use_cache):
                row_count = cache.get(f'dataset_{self.id}_row_count')
                if row_count is not None:
                    return row_count  
            engine = self.connection.engine_instance
            conn = engine.connect()
            query = text(f"SELECT COUNT(*) FROM {self.table_name}")
            cursor = conn.execute(query)
            conn.close()
            self.connection.disconnect()
            row_count = cursor.scalar()
            cache.set(f'dataset_{self.id}_row_count', row_count)
            return row_count
        except Exception as e:
            raise Exception(e)
        
    def get_dataset_plot_type(self):
        plot_type = []
        try:
            df = self.get_dataset_data()
            #  print the data type of each column
            print(df.dtypes)
            plot_type.append('pair_scatter_plot') # always return pair scatter plot
            # if dataset have numerical column, return histogram and pair scatter plot
            if 'int64' in df.dtypes.values or 'float64' in df.dtypes.values:
                plot_type.append('histogram')
            # if dataset have datetime column, return time series plot
            if 'datetime64[ns]' in df.dtypes.values:
                plot_type.append('time_series_plot')
            # if dataset have categorical column or boolean, return box plot and bar plot
            if 'object' in df.dtypes.values or 'bool' in df.dtypes.values:
                plot_type.append('box_plot')
                plot_type.append('bar_plot')
            return plot_type            

        except Exception as e:
            raise Exception(e)

    def __str__(self):
        return self.name
    
