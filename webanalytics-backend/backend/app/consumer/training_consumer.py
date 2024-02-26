from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from django.core.cache import cache

from ..models import Dataset
from AutoClean import AutoClean

from sklearn.preprocessing import StandardScaler, MinMaxScaler

import pandas as pd
import json
import redis
from tensorflow import keras

from ..services import MultilayerPerceptron

redis_instance = redis.StrictRedis(host='127.0.0.1', port=6379, db=1)

class TrainDatasetConsumer(AsyncWebsocketConsumer):   
    async def fetch_dataset(self, dataset_id) -> pd.DataFrame:
        # takes data from cache if exists, otherwise fetch from database
        try:
            df = await sync_to_async(cache.get)(f'dataset_{dataset_id}_data')
            if df is not None:
                return df
            else:
                dataset_instance = await sync_to_async(Dataset.objects.aget)(id=dataset_id)
                df = await sync_to_async(dataset_instance.get_dataset_data)()
                # await sync_to_async(cache.set)(f'dataset_{dataset_id}_data', df, timeout=60*60)
                return df
        except Exception as e:
            raise Exception(e)        
    
    async def train_dataset(self, request, dataset_id, features, target, X: pd.DataFrame, y: pd.DataFrame):
        try:
            if request['algorithm'] == "MLP":
                hidden_layers = request['parameters']['hidden_layers']
                #  task is classification if y is objects, otherwise regression
                task = 'classification' if pd.api.types.is_object_dtype(y) else 'regression'              
                await self.send(f"Training the dataset using Multilayer Perceptron algorithm...")
                mlp = await sync_to_async(MultilayerPerceptron)(
                    name=f"MLP-{dataset_id}", features=features, hidden_layers=hidden_layers, target=target, task=task, dataset_id=dataset_id
                )
                await self.send(await sync_to_async(mlp.summary)())           
                await sync_to_async(mlp.train)(X, y, epochs=request['parameters']['epochs'], batch_size=request['parameters']['batch_size'])
                await sync_to_async(mlp.save)()
                await sync_to_async(mlp.save_model_instance)()
                await self.send(f"Model saved successfully.")
        except Exception as e: 
            await self.send(str(e))        

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass    
    async def receive(self, text_data):
        """
        Train the dataset based on the selected algorithm
        format of the message:
        {
            "id": "dataset_id",
            "auto_clean": "True/False",
            "algorithm": "algorithm_name",
            "normalize": "True/False",
            "features": ["feature1", "feature2", ...]/all,
            "target": ["target_column", "target_column"]/all,
            "parameters": {
                "hidden_layers": [10, 5],
                "epochs": 20,
                "batch_size": 10                
            }            
        }
        """
        request = json.loads(text_data)
        try:
            dataset_id = request['id']
            features = request['features']
            target = request['target']
            df = await self.fetch_dataset(dataset_id)          
                        
            if request['auto_clean']:
                pr_df = AutoClean(df, mode='auto') 
                df = pr_df.output

            await self.send(f"Data cleaning completed, from {df.shape} to {pr_df.output.shape}")
            # get features from the request
            if request['features'] == "all":
                features = df.columns.to_list()
            # get target from the request
            if request['target'] == "all":
                target = df.columns.to_list()


            if request['normalize']:
                numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
                df[numeric_columns] = pd.DataFrame(StandardScaler().fit_transform(df[numeric_columns]), columns=numeric_columns)
                await self.send(f"Data normalization completed.")

            # get the features and target from the dataframe
            X = df[features]
            y = df[target]

            # await self.send(f"Features: {features}")
            # await self.send(f"Target: {target}")
            await self.train_dataset(request, dataset_id, features, target, X, y)

        except Exception as e:
            await self.send(str(e))
            
    
