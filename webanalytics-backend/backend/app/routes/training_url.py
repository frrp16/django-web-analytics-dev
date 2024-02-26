from ..consumer.training_consumer import TrainDatasetConsumer
from django.urls import include, path

training_url = [
    path(r'training/train', TrainDatasetConsumer.as_asgi()),
]