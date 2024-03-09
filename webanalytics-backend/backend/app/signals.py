from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification
from django.conf import settings

import pytz


@receiver(post_save, sender=Notification)
def create_notification(sender, instance, created, **kwargs):    
    if created:               
        # get instance.created_at as datetime
        date_create = instance.created_at.astimezone(pytz.timezone(settings.TIME_ZONE))

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"notification_{instance.user.id}",
            {
                "type": "send_notification",
                "notification": {   
                    "title": instance.title,
                    "message": instance.message,
                    "type": instance.type,
                    "context": instance.context,
                    # convert datetime to string with timezone
                    "created_at": date_create.strftime("%c")
                }
            }                
        )
