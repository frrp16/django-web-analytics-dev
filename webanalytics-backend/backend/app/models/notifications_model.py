from django.db import models
from django.contrib.auth.models import User

import uuid

class Notification(models.Model):     
    class NotificationType(models.TextChoices):
        INFO = 'INFO'
        SUCCESS = 'SUCCESS'
        WARNING = 'WARNING'
        ERROR = 'ERROR'
    class ContextType(models.TextChoices):
        AUTH = 'AUTH'
        CONNECTION = 'CONNECTION'
        DATASET = 'DATASET'
        TRAINING = 'TRAINING'
        PREDICTION = 'PREDICTION' 
        MONITORING = 'MONITORING'
        OTHER = 'OTHER'    
    class Meta:
        ordering = ['-created_at']
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='notifications')
    context = models.CharField(max_length=10, choices=ContextType.choices, default=ContextType.OTHER)
    type = models.CharField(max_length=7, choices=NotificationType.choices, default=NotificationType.INFO)    

    def __str__(self):
        return self.title