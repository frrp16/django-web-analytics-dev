from celery import shared_task
from celery.utils.log import get_task_logger

import pandas as pd

from celery.exceptions import MaxRetriesExceededError
from ..services.ml_service import MultilayerPerceptron, LSTM
from ..services.preprocess_service import ScaleDataService, CleanDataService
from ..services.dataset_service import update_training_status
from ..services.notification_service import create_notification

from celery.exceptions import MaxRetriesExceededError
import traceback

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
    hidden_layers: list | None,
    dataset_id: str,
    epochs: int,
    batch_size: int,  
    timesteps: int | None,
    user_id    
    ):
    try:
        logger.warn(f"Training model on dataset {dataset_id}")
        # logger.warn(pd.DataFrame(dataset).head())
        # Clean dataset
        clean_data_service = CleanDataService()
        preprocessed_df = clean_data_service.process(pd.DataFrame(dataset))
        
        # logger.warn(f"Features: {features}")
        # logger.warn(f"Target: {target}")
        # Set features and target
        logger.warn(preprocessed_df.head())
        X = pd.DataFrame(preprocessed_df[features])
        y = pd.DataFrame(preprocessed_df[target])

        # logger.warn(f"X: {X.head()}")
        # logger.warn(f"y: {y.head()}")

        logger.warn(f"Preprocessing completed for dataset {dataset_id}")
        
        if scaler:
            # Scale dataset
            scale_data_service = ScaleDataService(scaler)
            X = scale_data_service.process(X)

        logger.warn(f"Scaling completed for dataset {dataset_id}")

        # Create and train the model
        logger.warn(f"Training {algorithm} model on dataset {dataset_id}")
        
        match algorithm:
            case "MLP":
                if hidden_layers:
                    if not isinstance(hidden_layers, list):
                        hidden_layers = [hidden_layers]
                    model = MultilayerPerceptron(
                        name=name,
                        features=features,
                        target=target,
                        task=task,
                        dataset_id=dataset_id,
                        hidden_layers=hidden_layers
                    )
                else:
                    model = MultilayerPerceptron(
                        name=name,
                        features=features,
                        target=target,
                        task=task,
                        dataset_id=dataset_id
                    )
            case "LSTM":
                model = LSTM(
                    name=name,
                    features=features,
                    target=target,
                    task=task,
                    dataset_id=dataset_id,
                    timesteps=timesteps if timesteps else 5
                )
            case _:
                raise Exception("Invalid algorithm")
                 
        X_pd = X
        y_pd = y

        # logger.warn(f"X_pd type: {type(X_pd)}")
        # logger.warn(f"y_pd type: {type(y_pd)}")   

        # logger.warn(f"X_pd: {X_pd.head()}")
        # logger.warn(f"y_pd: {y_pd.head()}")                

        model.train(X_pd.values.astype('float32'), y_pd.values.astype('float32'), epochs, batch_size)                      

        logger.warn(f"{algorithm} model training completed for dataset {dataset_id}")   
        # Save the model
        logger.warn(f"Saving model instance {name}")
        model.save()
        model.save_model_instance(algorithm)
        update_training_status(dataset_id, 'TRAINED')   
        create_notification(
            "Model Training", 
            user_id, 
            f"Model '{name}' trained successfully.", 
            "SUCCESS",
            'TRAINING'
            )
        return True
    except Exception as e:
        logger.error(str(e))        
        try:
            self.retry(countdown=5)
        except MaxRetriesExceededError:
            update_training_status(dataset_id, 'UNTRAINED')
            create_notification(
                "Model Training", 
                user_id, 
                f"Model '{name}' training failed: {str(e)}.", 
                "ERROR",
                'TRAINING'
                )
            logger.error("Max retries exceeded. Task failed.")
        return False