from celery import shared_task
from celery.utils.log import get_task_logger

import pandas as pd

from celery.exceptions import MaxRetriesExceededError
from .services.ml_service import MultilayerPerceptron
from .services.preprocess_service import ScaleDataService, CleanDataService
from .services.dataset_service import update_training_status

from .models import DatasetMonitorLog

from django.utils import timezone
from celery.exceptions import MaxRetriesExceededError

logger = get_task_logger(__name__)

# Create celery task to train machine learning model
@shared_task(bind=True)
def train_model(
    self, 
    name,
    dataset, 
    features: list, 
    target: list,   
    scaler: str | None, 
    algorithm: str,
    task: str,
    hidden_layers: list,
    dataset_id: str,
    epochs: int,
    batch_size: int,  
    ):
    try:
        logger.info(f"Training model on dataset {dataset_id}")
        # Clean dataset
        clean_data_service = CleanDataService()
        preprocessed_df = clean_data_service.process(pd.DataFrame(dataset))
        
        logger.info(f"Features: {features}")
        logger.info(f"Target: {target}")
        # Set features and target
        X = preprocessed_df[features]
        y = preprocessed_df[target]

        logger.info(f"Preprocessing completed for dataset {dataset_id}")
        
        if scaler:
            # Scale dataset
            scale_data_service = ScaleDataService(scaler)
            X = scale_data_service.process(X)

        logger.info(f"Scaling completed for dataset {dataset_id}")

        # Create and train the model
        logger.info(f"Training {algorithm} model on dataset {dataset_id}")
        model = MultilayerPerceptron(
            name=name,
            features=features,
            target=target,
            hidden_layers=hidden_layers,
            task=task, 
            dataset_id=dataset_id
        )

        logger.info(model.summary())
        logger.info(f"Dataset shape: {X.shape}")                
        # logger.info(f"{X.head()}")
        # logger.info(f"{y.head()}")
        model.train(X.values.astype('float32'), y.values.astype('float32'), epochs, batch_size)                      

        logger.info(f"{algorithm} model training completed for dataset {dataset_id}")   
        # Save the model
        logger.info(f"Saving model instance {name}")
        model.save()
        model.save_model_instance()
        update_training_status(dataset_id, 'TRAINED')   
        return True
    except Exception as e:
        logger.error(e)
        try:
            self.retry(countdown=5)
        except MaxRetriesExceededError:
            update_training_status(dataset_id, 'UNTRAINED')
            logger.error("Max retries exceeded. Task failed.")
        return False
    
# @shared_task(bind=True, max_retries=100, soft_time_limit=300, time_limit=1500)
# def monitor_dataset(self):
#     try:
#         print("Run monitor_dataset task")
#         logger.info('Monitoring datasets...')
#         # get last updated monitor log per dataset
#         last_monitor_logs = DatasetMonitorLog.objects.order_by('dataset', '-timestamp').distinct('dataset')
#         for log in last_monitor_logs:
#             # check if last monitor log is 5 minutes old or more, if yes, update monitor log
#             if (timezone.now() - log.timestamp).seconds > 300:
#                 logger.info(f"Updating monitor log for dataset {log.dataset.name}")
#                 # get dataset
#                 dataset = Dataset.objects.get(id=log.dataset.id)  
#                 # create new monitor log            
#                 row_count = dataset.get_dataset_row_count()
#                 column_count = len(dataset.get_dataset_columns())
#                 monitor_log = DatasetMonitorLog(dataset=dataset, row_count=row_count, column_count=column_count)
#                 # Get last monitor log in order to compare
#                 last_monitor_log = DatasetMonitorLog.objects.filter(dataset=dataset).order_by('-timestamp').first()
#                 # if row count or column count is different from last monitor log, update monitor log
#                 if last_monitor_log.row_count != row_count or last_monitor_log.column_count != column_count:
#                     monitor_log.save()
#                     # get dataset instance and update status
#                     dataset.status = 'CHANGED'                    
#                     dataset.save(update_fields=['status'])
#                     logger.info(f"Monitor log for dataset {dataset.name} updated, Dataset status changed.")
#                 else:                    
#                     last_monitor_log.timestamp = timezone.now()
#                     last_monitor_log.save(update_fields=['timestamp'])
#                     logger.info(f"Monitor log for dataset {log.dataset.name} is up to date.")
#         return True
#     except Exception as e:
#         logger.error(f"An error occurred: {str(e)}")
#         try:
#             self.retry(countdown=5)
#         except MaxRetriesExceededError:
#             logger.error("Max retries exceeded. Task failed.")
#         return False
    
# # Create celery task to save model instance, takes class extended from BaseModel as input
# @shared_task(bind=True) 
# def save_model_instance(self, model_instance, dataset_id, access_token):
#     try:
#         logger.info(f"Saving model instance {model_instance.name}")
#         model_instance.save()
#         model_instance.save_model_instance()
#         update_training_status(dataset_id, 'TRAINED', access_token)
#         return True 
#     except Exception as e:
#         logger.error(e)
#         try:
#             self.retry(countdown=5)
#         except MaxRetriesExceededError:
#             update_training_status(dataset_id, 'UNTRAINED', access_token)
#             logger.error("Max retries exceeded. Task failed.")
#         return False