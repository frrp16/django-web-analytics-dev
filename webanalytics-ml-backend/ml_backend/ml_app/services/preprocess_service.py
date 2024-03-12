import pandas as pd
from pandas.api.types import is_bool_dtype
import traceback

from sklearn.preprocessing import StandardScaler, MinMaxScaler
# isolation forest for outlier detection
from sklearn.ensemble import IsolationForest

class CleanDataService:
    def process(self, dataset: pd.DataFrame) -> pd.DataFrame:
        try:    
            # drop columns with all missing values
            df = dataset.dropna(axis=1, how='all')
            # drop rows with all missing values
            df = df.dropna(axis=0, how='all')            

            # fill missing values
            df = df.fillna(df.mode().iloc[0])

            # encode object columns
            for col in df.columns:
                if df[col].dtype == 'object':
                    df[col] = df[col].astype('category').cat.codes

            # encode boolean columns
            for col in df.columns:
                if is_bool_dtype(df[col]):
                    df[col] = df[col].astype(int)

            # Handling outlier using Isolation Forest
            # define outlier detection model
            model = IsolationForest(contamination=0.1)
            # fit on dataset
            model.fit(df)
            # detect outliers in the dataset
            yhat = model.predict(df)
            # select all rows that are not outliers
            mask = yhat != -1
            df = df[mask]

            return df

            

        except Exception as e:
            traceback.print_exc()
            raise Exception(e)

class ScaleDataService:
    def __init__(self, method: str) -> None:
        self.method = method
        self.scaling_method = self.scaling_method

    def scaling_method(self):
        if self.method == 'StandardScaler':
            return StandardScaler()
        elif self.method == 'MinMaxScaler':
            return MinMaxScaler()
        else:
            return None

    def process(self, dataset: pd.DataFrame) -> pd.DataFrame:
        try:            
            df = dataset
            if self.scaling_method != None:
                numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
                scaled_df = df.copy()
                scaled_df[numeric_columns] = pd.DataFrame(self.scaling_method().fit_transform(df[numeric_columns]), columns=numeric_columns)            
            else:
                return None
            return scaled_df
        except Exception as e:
            raise Exception(e)

class SampleDataService:
    def __init__(self, count, frac=0) -> None:
        self.frac = frac
        self.count = count

    def process(self, dataset: pd.DataFrame) -> pd.DataFrame:
        try:
            return dataset.sample(frac=self.frac, random_state=1) if self.frac else dataset.sample(n=self.count, random_state=1)
        except Exception as e:
            raise Exception(e)
