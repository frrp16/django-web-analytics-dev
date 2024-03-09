from celery import shared_task
from celery.utils.log import get_task_logger

import pandas as pd

from celery.exceptions import MaxRetriesExceededError

from ..services.dataset_service import get_dataset_columns, update_dataset_change_status, get_dataset_row_count, get_dataset_instance
from ..services.notification_service import create_notification
from ..models import DatasetMonitorLog
from django.utils import timezone

logger = get_task_logger(__name__)
    
@shared_task(bind=True, max_retries=5, time_limit=300)
def monitor_dataset(self):
    try:
        print("Run monitor_dataset task")
        logger.info('Monitoring datasets...')
        # get last updated monitor log per dataset
        last_monitor_logs = DatasetMonitorLog.objects.order_by('dataset', '-timestamp').distinct('dataset')
        for log in last_monitor_logs:
            # check if last monitor log is 5 minutes old or more, if yes, update monitor log
            if (timezone.now() - log.timestamp).seconds > 300:
                logger.info(f"Updating monitor log for dataset {log.dataset}")                
                dataset = log.dataset                                
                row_count = get_dataset_row_count(dataset)
                column_count = len(get_dataset_columns(dataset))
                monitor_log = DatasetMonitorLog(dataset=dataset, row_count=row_count, column_count=column_count)                
                last_monitor_log = DatasetMonitorLog.objects.filter(dataset=dataset).order_by('-timestamp').first()

                if last_monitor_log.row_count != row_count or last_monitor_log.column_count != column_count:
                    monitor_log.save()                    
                    change_dataset_status.delay(dataset, 'CHANGED')
                else:                    
                    last_monitor_log.timestamp = timezone.now()
                    last_monitor_log.save(update_fields=['timestamp'])
                    change_dataset_status.delay(dataset, 'STABLE')
        return True
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        try:
            self.retry(countdown=5)
        except MaxRetriesExceededError:
            logger.error("Max retries exceeded. Task failed.")
        return False


@shared_task(bind=True, max_retries=10, soft_time_limit=300, time_limit=1500)
def monitor_single_dataset(self, dataset_id):
    try:
        print("Run monitor_single_dataset task")
        logger.info(f"Monitoring dataset {dataset_id}...")        
        last_monitor_log = DatasetMonitorLog.objects.filter(dataset=dataset_id).order_by('-timestamp').first()  
                   
        logger.info(f"Updating monitor log for dataset {dataset_id}")                        
        row_count = get_dataset_row_count(dataset_id)
        column_count = len(get_dataset_columns(dataset_id))
        monitor_log = DatasetMonitorLog(dataset=dataset_id, row_count=row_count, column_count=column_count)
        
        if last_monitor_log.row_count != row_count or last_monitor_log.column_count != column_count:
            monitor_log.unacknowledged_rows = row_count - last_monitor_log.row_count
            monitor_log.save()
            change_dataset_status.delay(dataset_id, 'CHANGED')
        else:                    
            last_monitor_log.timestamp = timezone.now()
            last_monitor_log.save(update_fields=['timestamp'])
            change_dataset_status.delay(dataset_id, 'STABLE', True)
        return True
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        try:
            self.retry(countdown=5)
        except MaxRetriesExceededError:
            change_dataset_status.delay(dataset_id, 'ERROR')
        return False


@shared_task(bind=True)
def change_dataset_status(self, dataset_id, status, manual=False):        
    dataset_instance = get_dataset_instance(dataset_id=dataset_id)
    if status == 'CHANGED':
        update_dataset_change_status(dataset_id, status)        
        create_notification(
            "Monitor Log", 
            dataset_instance["user"], 
            f"Monitor log for dataset '{dataset_instance['name']}' updated, Dataset status changed.", 
            "INFO",
            'MONITORING'
            )              
        logger.warn(f"Monitor log for dataset {dataset_id} updated, Dataset status changed.")

    elif status == 'STABLE':
        if manual:
            create_notification(
                    "Monitor Log", 
                    dataset_instance["user"], 
                    f"Monitor log for dataset '{dataset_instance['name']}' is up to date.", 
                    "INFO",
                    'MONITORING'
                    )
        logger.info(f"Monitor log for dataset {dataset_id} is up to date.")

    elif status == 'ERROR':
        create_notification(
                "Monitor Log", 
                dataset_instance["user"], 
                f"Monitor log for dataset '{dataset_instance['name']}' failed to update.", 
                "ERROR",
                'MONITORING'
            )
        logger.error("Max retries exceeded. Task failed.")
    return True