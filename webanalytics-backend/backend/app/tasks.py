from celery import shared_task
from celery.utils.log import get_task_logger

from .models import Dataset, DatasetMonitorLog
from django.utils import timezone
from celery.exceptions import MaxRetriesExceededError

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
                logger.info(f"Updating monitor log for dataset {log.dataset.name}")
                # get dataset
                dataset = Dataset.objects.get(id=log.dataset.id)  
                # create new monitor log            
                row_count = dataset.get_dataset_row_count()
                column_count = len(dataset.get_dataset_columns())
                monitor_log = DatasetMonitorLog(dataset=dataset, row_count=row_count, column_count=column_count)
                # Get last monitor log in order to compare
                last_monitor_log = DatasetMonitorLog.objects.filter(dataset=dataset).order_by('-timestamp').first()
                # if row count or column count is different from last monitor log, update monitor log
                if last_monitor_log.row_count != row_count or last_monitor_log.column_count != column_count:
                    monitor_log.save()
                    # get dataset instance and update status
                    dataset.status = 'CHANGED'                    
                    dataset.save(update_fields=['status'])
                    logger.info(f"Monitor log for dataset {dataset.name} updated, Dataset status changed.")
                else:                    
                    last_monitor_log.timestamp = timezone.now()
                    last_monitor_log.save(update_fields=['timestamp'])
                    logger.info(f"Monitor log for dataset {log.dataset.name} is up to date.")
        return True
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        try:
            self.retry(countdown=5)
        except MaxRetriesExceededError:
            logger.error("Max retries exceeded. Task failed.")
        return False

# @shared_task
# def train_linear_regression(dataset):
#     try:
#         logger.info(f"Training Linear Regression on dataset {dataset.name}")
#         # Perform data preprocessing and feature engineering
#         X, y = preprocess_dataset(dataset)
        
#         # Create and train the Linear Regression model
#         model = LinearRegression()
#         model.fit(X, y)
        
#         # Save the trained model
#         save_model(model, dataset)
        
#         logger.info(f"Linear Regression training completed for dataset {dataset.name}")
#         return True
#     except Exception as e:
#         logger.error(f"An error occurred while training Linear Regression: {str(e)}")
#         return False

# def preprocess_dataset(dataset):
#     # Perform data preprocessing and feature engineering here
#     # Return the preprocessed features (X) and target variable (y)
#     pass

# def save_model(model, dataset):
#     # Save the trained model to a file or database
#     pass


# create test task to check if celery is working
@shared_task
def test_task():
    logger.info('Test task is working')
