from celery import shared_task
from celery.utils.log import get_task_logger

import pandas as pd
import numpy as np
import dotenv
import ast

from celery.exceptions import MaxRetriesExceededError
from ..services.preprocess_service import CleanDataService, ScaleDataService
from ..services.dataset_service import get_dataset_data, update_training_status, get_dataset_instance
from ..services.notification_service import create_notification

from ..models import MLModel

from celery.exceptions import MaxRetriesExceededError
import traceback

logger = get_task_logger(__name__)



@shared_task(bind=True)
def train_model(self, models_id):
    try:
        model_instance = MLModel.objects.get(id=models_id)
        logger.warn(f"Training model {model_instance.name} on dataset {str(model_instance.dataset)}")

        # Get dataset data
        logger.warn(f"Getting dataset {str(model_instance.dataset)} data...")
        df = pd.DataFrame(get_dataset_data(model_instance.dataset))
        dataset_instance = get_dataset_instance(model_instance.dataset)

        # Merge features and target array
        logger.warn(f"Processing dataset {str(model_instance.dataset)}...")
        features_list = ast.literal_eval(model_instance.features)
        target_list = ast.literal_eval(model_instance.target)

        columns = list(set(features_list + target_list))
        df = df[columns]

        # Clean dataset 
        logger.warn(f"Cleaning dataset {str(model_instance.dataset)}...")
        clean_data_service = CleanDataService()
        preprocessed_df = clean_data_service.process(df)

        # Sample dataset
        logger.warn(f"Sampling dataset {str(model_instance.dataset)}...")
        if model_instance.sample_size:
             preprocessed_df = preprocessed_df.sample(n=model_instance.sample_size, random_state=1)
        else:
            preprocessed_df = preprocessed_df.sample(frac=model_instance.sample_frac, random_state=1)
        if model_instance.algorithm == "LSTM":
            preprocessed_df = preprocessed_df.sort_index()
        
        logger.warn(f"Features: {features_list}")
        logger.warn(f"Target: {target_list}")

        # Set features and target
        X = pd.DataFrame(preprocessed_df[features_list])
        y = pd.DataFrame(preprocessed_df[target_list])

        logger.warn(f"X shape: {X.shape}")
        logger.warn(f"y shape: {y.shape}")

        logger.warn(f"X dtype: {X.dtypes}")
        logger.warn(f"y dtype: {y.dtypes}")

        # Scale dataset
        logger.warn(f"Scaling dataset {str(model_instance.dataset)}...")
        if model_instance.scaler:
            scale_data_service = ScaleDataService(model_instance.scaler)
            X = scale_data_service.process(X)

        
        X = X.values.astype(np.float32)
        # if task is classification or binary, convert y to int
        if model_instance.task == "Classification" or model_instance.task == "Binary":
            y = y.values.astype(int)
        else:
            y = y.values.astype(np.float32)
        
        # Create and train the model
        logger.warn(f"Training {model_instance.algorithm} model on dataset {str(model_instance.dataset)}")
        model_instance.train(X, y)

        logger.warn(f"{model_instance.algorithm} model training completed for dataset {str(model_instance.dataset)}") 
        create_notification(
            title="Model trained successfully",
            message=f"{model_instance.algorithm} model training completed for dataset {str(dataset_instance['name'])}",
            context="TRAINING",
            type="SUCCESS",
            user=dataset_instance["user"]
        )
    
    except Exception as e:
        traceback.print_exc()
        logger.error(str(e))
        try:
            self.retry(countdown=5)
        except MaxRetriesExceededError:
                create_notification(
                    title="Model trained failed",
                    message=f"{model_instance.algorithm} model training failed for dataset {str(dataset_instance['name'])}",
                    context="TRAINING",
                    type="ERROR",
                    user=dataset_instance["user"]
                )
                logger.error("Max retries exceeded. Task failed.")
        return False