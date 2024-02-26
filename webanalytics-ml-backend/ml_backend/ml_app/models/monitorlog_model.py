from django.db import models

import uuid


class DatasetMonitorLog(models.Model):
   id  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
   timestamp = models.DateTimeField(auto_now_add=True)
   dataset = models.CharField(max_length=255, null=True)
   row_count = models.IntegerField(default=0)
   column_count = models.IntegerField(default=0)   