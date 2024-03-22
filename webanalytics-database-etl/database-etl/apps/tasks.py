from celery import shared_task
from celery.utils.log import get_task_logger
from celery.exceptions import MaxRetriesExceededError

from django.utils import timezone
import pandas as pd

from .models import DatasetTable, DatasetMonitorLog

from .api import create_notification, get_dataset_instance

@shared_task(bind=True, max_retries=5)
def load_data_task(self, dataset_table_id, new_table=False):
    logger = get_task_logger(__name__)
    try:        
        dataset_table = DatasetTable.objects.get(pk=dataset_table_id)
        dataset_instance = get_dataset_instance(dataset_table_id)
        # Get data
        old_dataset_data = dataset_table.get_data_from_warehouse() if new_table == False else None
        dataset_data = dataset_table.extract_data()
        # Load data
        dataset_table.load_data(dataset_data)
        row_count = len(dataset_data)
        column_count = len(dataset_data.columns.to_list())
        # Check for changes        
        changes = find_data_changes(old_dataset_data, dataset_data) if new_table == False else {}
        # Update time updated
        dataset_table.date_updated = timezone.now()
        dataset_table.save()
        # Save log
        dataset_monitor_log = DatasetMonitorLog(
            dataset_table=dataset_table, row_count=row_count, column_count=column_count, changes=changes
        )
        dataset_monitor_log.save()        
        create_notification(
            title="Dataset Load Success",
            message=f"Dataset {dataset_table.table_name} loaded successfully. {row_count} rows and {column_count} columns loaded.",
            context="DATASET",
            type="SUCCESS",
            user=dataset_instance["user"]
        )
        if not new_table and (changes['added_rows']  or changes['modified_rows'] or changes['deleted_rows']):	
            create_notification(
                title="Dataset Changes Detected",
                message=f"Dataset {dataset_table.table_name} has changes with {len(changes['added_rows'])} added rows, {len(changes['modified_rows'])} modified rows and {len(changes['deleted_rows'])} deleted rows.",
                context="DATASET",
                type="WARNING",
                user=dataset_instance["user"]
            )
        return f"Dataset {dataset_table.table_name} loaded successfully. {row_count} rows and {column_count} columns loaded."
    except Exception as e:
        logger.error(e)
        try:
            self.retry(countdown=5, exc=e)
        except MaxRetriesExceededError:
            logger.error("Max retries exceeded. Task failed.")
            create_notification(
            title="Dataset Load Failed",
            message=f"Dataset {dataset_table.table_name} loaded failed. {str(e)}",
            context="DATASET",
            type="ERROR",
            user=dataset_instance["user"]
        )
            return False

@shared_task(bind=True, max_retries=100)
def periodic_load_all_data(self):
    logger = get_task_logger(__name__)
    try:
        dataset_tables = DatasetTable.objects.all()
        for dataset_table in dataset_tables:
            if dataset_table.date_updated < timezone.now() - timezone.timedelta(days=1):
                logger.warn(f"Load datase {dataset_table.table_name} from database {dataset_table.connection.database}.")
                load_data_task.delay(dataset_table.id)                 
        return True
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        try:
            self.retry(countdown=5)
        except MaxRetriesExceededError:
            logger.error("Max retries exceeded. Task failed.")
        return False


def find_data_changes(existing_data: pd.DataFrame, new_data: pd.DataFrame):
    """
    Compare existing data with new data to detect changes.
    """
    changes = {}
    
    # Check for added rows
    added_rows = new_data[~new_data.index.isin(existing_data.index)]
    # if not added_rows.empty:
    changes['added_rows'] = added_rows.reset_index(drop=True)
        
    # Check for modified rows
    modified_rows = new_data.merge(existing_data, indicator=True, how='outer')
    modified_rows = modified_rows[modified_rows['_merge'] == 'left_only'].drop(columns=['_merge'])
    # if not modified_rows.empty:
    changes['modified_rows'] = modified_rows.reset_index(drop=True)
        
    # Check for deleted rows
    deleted_rows = existing_data[~existing_data.index.isin(new_data.index)]
    # if not deleted_rows.empty:
    changes['deleted_rows'] = deleted_rows.reset_index(drop=True)

    # changes all timestamp data in added_rows, modified_rows and deleted_rows to string
    df_temp = changes['added_rows'].select_dtypes(include=['datetime'])
    for col in df_temp.columns:
        changes['added_rows'][col] = changes['added_rows'][col].dt.strftime('%Y-%m-%d %H:%M:%S')
    df_temp = changes['modified_rows'].select_dtypes(include=['datetime'])
    for col in df_temp.columns:
        changes['modified_rows'][col] = changes['modified_rows'][col].dt.strftime('%Y-%m-%d %H:%M:%S')
    df_temp = changes['deleted_rows'].select_dtypes(include=['datetime'])
    for col in df_temp.columns:
        changes['deleted_rows'][col] = changes['deleted_rows'][col].dt.strftime('%Y-%m-%d %H:%M:%S')
    

    changes['added_rows'] = changes['added_rows'].to_dict(orient='records')
    changes['modified_rows'] = changes['modified_rows'].to_dict(orient='records')
    changes['deleted_rows'] = changes['deleted_rows'].to_dict(orient='records')
        
    return changes