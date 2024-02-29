from celery import shared_task
from celery.utils.log import get_task_logger

import pandas as pd

from celery.exceptions import MaxRetriesExceededError

from ..services.dataset_service import get_dataset_columns, update_dataset_change_status, get_dataset_row_count
from ..models import DatasetMonitorLog
from django.utils import timezone

logger = get_task_logger(__name__)
    
@shared_task(bind=True, max_retries=100, soft_time_limit=300, time_limit=1500)
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
                # get dataset
                # dataset = get_dataset_instance(log.dataset)
                dataset = log.dataset
                # create new monitor log            
                row_count = get_dataset_row_count(dataset)
                column_count = len(get_dataset_columns(dataset))
                monitor_log = DatasetMonitorLog(dataset=dataset, row_count=row_count, column_count=column_count)
                # Get last monitor log in order to compare
                last_monitor_log = DatasetMonitorLog.objects.filter(dataset=dataset).order_by('-timestamp').first()
                # if row count or column count is different from last monitor log, update monitor log
                if last_monitor_log.row_count != row_count or last_monitor_log.column_count != column_count:
                    monitor_log.save()
                    # get dataset instance and update status
                    status = 'CHANGED'   
                    update_dataset_change_status(dataset.id, status)                      
                    logger.info(f"Monitor log for dataset {dataset} updated, Dataset status changed.")
                else:                    
                    last_monitor_log.timestamp = timezone.now()
                    last_monitor_log.save(update_fields=['timestamp'])
                    logger.info(f"Monitor log for dataset {dataset} is up to date.")
        return True
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        try:
            self.retry(countdown=5)
        except MaxRetriesExceededError:
            logger.error("Max retries exceeded. Task failed.")
        return False
