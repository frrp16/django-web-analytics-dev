from celery import shared_task
from celery.utils.log import get_task_logger

import pandas as pd

from celery.exceptions import MaxRetriesExceededError
from .services.ml_service import MultilayerPerceptron
from .services.preprocess_service import ScaleDataService, CleanDataService
from .services.dataset_service import update_training_status

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
    access_token: str  
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
        update_training_status(dataset_id, 'TRAINED', access_token)   
        return True
    except Exception as e:
        logger.error(e)
        try:
            self.retry(countdown=5)
        except MaxRetriesExceededError:
            update_training_status(dataset_id, 'UNTRAINED', access_token)
            logger.error("Max retries exceeded. Task failed.")
        return False
    
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