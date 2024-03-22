from django.db import models
from django.core.cache import cache
from django.contrib.auth.models import User

from .connection_model import DatabaseConnection

import uuid
import pandas as pd
import json 
import dotenv
import os

dotenv.load_dotenv()

from sqlalchemy import create_engine, URL, text

database_etl_url = URL.create(
    drivername='postgresql',
    username=os.getenv('WAREHOUSE_DATABASE_USER'),
    password=os.getenv('WAREHOUSE_DATABASE_PASSWORD'),
    host=os.getenv('WAREHOUSE_DATABASE_HOST'),
    port=os.getenv('WAREHOUSE_DATABASE_PORT'),
    database=os.getenv('WAREHOUSE_DATABASE_NAME')
)

database_etl_engine = create_engine(database_etl_url)

class Dataset(models.Model):
    """
    Represents a dataset in the application.

    Attributes:
        id (UUIDField): The unique identifier of the dataset.
        name (CharField): The name of the dataset.
        description (TextField): The description of the dataset.
        table_name (CharField): The name of the table associated with the dataset.
        created_at (DateTimeField): The timestamp when the dataset was created.
        status (CharField): The status of the dataset (CHANGED or STABLE).
        is_trained (CharField): The training status of the dataset (TRAINING, TRAINED, or UNTRAINED).
        user (ForeignKey): The user who owns the dataset.
        connection (ForeignKey): The database connection associated with the dataset.

    Methods:
        get_dataset_data(): Retrieves the dataset data from the database.
        get_dataset_columns_type(use_cache=False): Retrieves the column names and types of the dataset.
        get_dataset_row_count(use_cache=False): Retrieves the row count of the dataset.
        get_dataset_plot_type(): Retrieves the plot types that can be generated for the dataset.
    """

    class DatasetStatus(models.TextChoices):
        CHANGED = 'CHANGED'
        STABLE = 'STABLE'

    class DatasetTrainingStatus(models.TextChoices):
        TRAINING = 'TRAINING'
        TRAINED = 'TRAINED'
        UNTRAINED = 'UNTRAINED'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    table_name = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=7, choices=DatasetStatus.choices, default=DatasetStatus.STABLE)
    is_trained = models.CharField(max_length=9, choices=DatasetTrainingStatus.choices, default=DatasetTrainingStatus.UNTRAINED)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='datasets')
    connection = models.ForeignKey(DatabaseConnection, on_delete=models.CASCADE, null=True)

    def get_dataset_data(self):
        """
        Retrieves the dataset data from the database.

        Returns:
            DataFrame: The dataset data as a pandas DataFrame.

        Raises:
            Exception: If an error occurs while retrieving the dataset data.
        """
        try:
            df = cache.get(f'dataset_{self.id}_data')
            if df is not None:
                return df
            else:
                engine = database_etl_engine
                # if database table is exist
                if engine.dialect.has_table(engine.connect(), f"{self.connection.database}_{self.table_name}"):
                    df = pd.read_sql_table(str(f"{self.connection.database}_{self.table_name}"), con=engine) 
                    cache.set(f'dataset_{self.id}_data', df)
                    engine.dispose()
                    return df
                else:                    
                    return False
        except Exception as e:
            raise Exception(e)

    def get_dataset_columns_type(self, use_cache=False):
        """
        Retrieves the column names and types of the dataset.

        Args:
            use_cache (bool, optional): Whether to use the cached column names and types. Defaults to False.

        Returns:
            list: A list of dictionaries containing the column names and types.

        Raises:
            Exception: If an error occurs while retrieving the column names and types.
        """
        try:
            if use_cache:
                columns_type = cache.get(f'dataset_{self.id}_columns_type')
                if columns_type is not None:
                    return columns_type

            df = self.get_dataset_data()
            if df is False:
                return False
            columns_type_dict = df.dtypes.astype(str).to_dict()
            columns_type = [{"column": column, "type": dtype} for column, dtype in columns_type_dict.items()]
            cache.set(f'dataset_{self.id}_columns_type', columns_type)             
            return columns_type
        except Exception as e:
            raise Exception(e)

    def get_dataset_row_count(self, use_cache=False):
        """
        Retrieves the row count of the dataset.

        Args:
            use_cache (bool, optional): Whether to use the cached row count. Defaults to False.

        Returns:
            int: The row count of the dataset.

        Raises:
            Exception: If an error occurs while retrieving the row count.
        """
        try:
            if (use_cache):
                row_count = cache.get(f'dataset_{self.id}_row_count')
                if row_count is not None:
                    return row_count  
            engine = database_etl_engine
            conn = engine.connect()
            query = text(f"SELECT COUNT(*) FROM {self.connection.database}_{self.table_name}")
            cursor = conn.execute(query)
            conn.close()
            self.connection.disconnect()
            row_count = cursor.scalar()
            cache.set(f'dataset_{self.id}_row_count', row_count)
            return row_count
        except Exception as e:
            raise Exception(e)

    def get_dataset_plot_type(self):
        """
        Retrieves the plot types that can be generated for the dataset.

        Returns:
            list: A list of plot types.

        Raises:
            Exception: If an error occurs while retrieving the plot types.
        """
        plot_type = []
        try:
            df = self.get_dataset_data()
            #  print the data type of each column
            print(df.dtypes)
            plot_type.append('pair_scatter_plot') # always return pair scatter plot
            # if dataset have numerical column, return histogram and pair scatter plot
            if 'int64' in df.dtypes.values or 'float64' in df.dtypes.values:
                plot_type.append('histogram')
            # if dataset have datetime column, return time series plot
            if 'datetime64[ns]' in df.dtypes.values:
                plot_type.append('time_series_plot')
            # if dataset have categorical column or boolean, return box plot and bar plot
            if 'object' in df.dtypes.values or 'bool' in df.dtypes.values:
                plot_type.append('box_plot')
                plot_type.append('bar_plot')
            return plot_type            

        except Exception as e:
            raise Exception(e)

    def __str__(self):
        return self.name
    
