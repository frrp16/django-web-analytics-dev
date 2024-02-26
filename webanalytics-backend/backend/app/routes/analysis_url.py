from ..consumer.analysis_consumer import LoadDataConsumer, DescriptiveStatisticsConsumer, FeatureCorrelationConsumer
from django.urls import include, path

analysis_url = [
    path(r'analysis/load', LoadDataConsumer.as_asgi()),
    path(r'analysis/describe', DescriptiveStatisticsConsumer.as_asgi()),
    path(r'analysis/correlation', FeatureCorrelationConsumer.as_asgi()),
]