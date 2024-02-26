from django.db import models
from .dataset_model import Dataset

import uuid


class DatasetMonitorLog(models.Model):
   id  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
   timestamp = models.DateTimeField(auto_now_add=True)
   dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='monitor_logs')
   row_count = models.IntegerField(default=0)
   column_count = models.IntegerField(default=0)   