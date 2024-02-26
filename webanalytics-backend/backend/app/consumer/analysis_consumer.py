from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from ..models import Dataset

import pandas as pd
import json

class LoadDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept() 

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # takes parameter from the message that contains array of column names
        dataset_id = json.loads(text_data)['id']    
        try:
            columns = json.loads(text_data)['columns']        
            # will filter the dataset content by column                
            if columns != "all":
                # convert column string to array                
                dataset_instance = await Dataset.objects.aget(id=dataset_id)
                df = await sync_to_async(dataset_instance.get_dataset_data)()
                df = df[columns]
                await self.send(str(df.to_dict(orient='records'))) 
            else:
                dataset_instance = await Dataset.objects.aget(id=dataset_id)
                df = await sync_to_async(dataset_instance.get_dataset_data)()
                await self.send(str(df.to_dict(orient='records')))
        except Exception as e:
            await self.send(str(e))

class DescriptiveStatisticsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        try:
            dataset_id = json.loads(text_data)['id']
            dataset_instance = await Dataset.objects.aget(id=dataset_id)
            df = await sync_to_async(dataset_instance.get_dataset_data)()
            descriptive_statistics = df.describe(include='all')
            await self.send(str(descriptive_statistics.to_dict()))
        except Exception as e:
            await self.send(str(e))

class FeatureCorrelationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        try:
            # parse JSON from message
            dataset_id = json.loads(text_data)['id']
            dataset_instance = await Dataset.objects.aget(id=dataset_id)
            df = await sync_to_async(dataset_instance.get_dataset_data)()
            feature_correlation = df.corr(numeric_only=True)
            await self.send(str(feature_correlation.to_dict()))
        except Exception as e:
            await self.send(str(e))