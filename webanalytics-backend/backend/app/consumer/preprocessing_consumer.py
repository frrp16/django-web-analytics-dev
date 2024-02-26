from channels.generic.websocket import AsyncWebsocketConsumer
import json
import pandas as pd
from AutoClean import AutoClean
from ..models import Dataset
from asgiref.sync import sync_to_async

from sklearn.preprocessing import StandardScaler, MinMaxScaler

class CleanDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data): 
        try:
            dataset_id = json.loads(text_data)['id']
            dataset_instance = await Dataset.objects.aget(id=dataset_id)
            df = await sync_to_async(dataset_instance.get_dataset_data)()
            preprocessed_df = AutoClean(df, mode='auto')

            await self.send(
                str(preprocessed_df.output.to_dict(orient='records'))
            )
        except Exception as e:
            await self.send(str(e))


class ScaleDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        try:
            dataset_id = json.loads(text_data)['id']
            scaling_method = json.loads(text_data)['method']
            dataset_instance = await Dataset.objects.aget(id=dataset_id)
            df = await sync_to_async(dataset_instance.get_dataset_data)()
            if scaling_method == 'standard':
                numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
                scaled_df = df.copy()
                scaled_df[numeric_columns] = pd.DataFrame(StandardScaler().fit_transform(df[numeric_columns]), columns=numeric_columns)
            elif scaling_method == 'minmax':
                numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
                scaled_df = df.copy()
                scaled_df[numeric_columns] = pd.DataFrame(MinMaxScaler().fit_transform(df[numeric_columns]), columns=numeric_columns)
            else:
                await self.send("Invalid scaling method")
            await self.send(str(scaled_df.to_dict(orient='records')))
           
        except Exception as e:
            await self.send(str(e))