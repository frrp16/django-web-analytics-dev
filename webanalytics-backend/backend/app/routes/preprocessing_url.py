from ..consumer.preprocessing_consumer import CleanDataConsumer, ScaleDataConsumer
from django.urls import include, path

preprocesssing_url = [
    path(r'preprocessing/clean', CleanDataConsumer.as_asgi()),
    path(r'preprocessing/scale', ScaleDataConsumer.as_asgi()),
]