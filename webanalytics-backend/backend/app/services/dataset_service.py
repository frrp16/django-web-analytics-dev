from django.contrib.auth.models import User
from django.core.cache import cache

from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError

from ..models import Dataset, DatabaseConnection, DatasetMonitorLog
from ..services import get_user_from_token

import pandas as pd

def create_dataset(name, description, table_name, token):
    try:
        user_instance = get_user_from_token(token)
        
        db_connection = DatabaseConnection.objects.get(user=user_instance.id)
        engine = db_connection.engine_instance
        df = pd.read_sql_table(table_name, con=engine)   
        column_count = len(df.columns)
        row_count = len(df.index)
        
        dataset_instance = Dataset(
            name=name, description=description, table_name=table_name, 
            user=user_instance, connection=db_connection,
        )
        dataset_instance.save()
        
        monitor_log_instance = DatasetMonitorLog(
            dataset=dataset_instance, row_count=row_count, column_count=column_count
        )
        monitor_log_instance.save()
        
        engine.dispose()
        return dataset_instance, None
    except Exception as e:
        return None, str(e)

def get_dataset_data(pk, order, column, asc):
    try:
        df = cache.get(f'dataset_{pk}_data')
        if df is None:
            dataset_instance = Dataset.objects.get(id=pk)
            df = dataset_instance.get_dataset_data()
            cache.set(f'dataset_{pk}_data', df, timeout=60*60)                      
        
        for column in df.columns:
            if df[column].isnull().sum() > 0 and df[column].dtype in ['int64', 'float64']:
                df[column].fillna(0, inplace=True)
            elif df[column].isnull().sum() > 0 and df[column].dtype == 'object':
                df[column].fillna('-', inplace=True) 
        
        if order and column:
            df = df.sort_values(by=[column], ascending=asc)    
        
        return df.to_dict(orient='records'), None
    except Exception as e:
        return None, str(e)