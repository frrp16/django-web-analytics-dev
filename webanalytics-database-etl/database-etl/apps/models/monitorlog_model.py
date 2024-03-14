from django.db import models

from .dataset_model import DatasetTable

import uuid

class DatasetMonitorLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    dataset_table = models.ForeignKey(DatasetTable, on_delete=models.CASCADE)
    date_updated = models.DateTimeField(auto_now=True)
    row_count = models.IntegerField()
    column_count = models.IntegerField()  
    changes = models.JSONField(null=True)  