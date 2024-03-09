from celery import shared_task
from celery.utils.log import get_task_logger
from celery.exceptions import MaxRetriesExceededError

from django.utils import timezone

from .models import DatasetTable, DatasetMonitorLog

from .api import create_notification

@shared_task(bind=True, max_retries=5)
def load_data_task(self, dataset_table_id):
    logger = get_task_logger(__name__)
    try:        
        dataset_table = DatasetTable.objects.get(pk=dataset_table_id)
        dataset_data = dataset_table.extract_data()
        dataset_table.load_data(dataset_data)
        row_count = len(dataset_data)
        column_count = len(dataset_data.columns.to_list())
        # Update time updated
        dataset_table.date_updated = timezone.now()
        dataset_table.save()
        # Save log
        dataset_monitor_log = DatasetMonitorLog(
            dataset_table=dataset_table, row_count=row_count, column_count=column_count
        )
        dataset_monitor_log.save()        
        return f"Dataset {dataset_table.table_name} loaded successfully. {row_count} rows and {column_count} columns loaded."
    except Exception as e:
        logger.error(e)
        try:
            self.retry(countdown=5, exc=e)
        except MaxRetriesExceededError:
            logger.error("Max retries exceeded. Task failed.")
            return False

@shared_task(bind=True)
def periodic_load_all_data(self):
    logger = get_task_logger(__name__)
    try:
        dataset_tables = DatasetTable.objects.all()
        for dataset_table in dataset_tables:
            if dataset_table.date_updated < timezone.now() - timezone.timedelta(days=1):
                load_data_task.delay(dataset_table.id)                
        return True
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        try:
            self.retry(countdown=5)
        except MaxRetriesExceededError:
            logger.error("Max retries exceeded. Task failed.")
        return False

