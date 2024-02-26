import pandas as pd
from AutoClean import AutoClean

from sklearn.preprocessing import StandardScaler, MinMaxScaler

class CleanDataService:
    def process(self, dataset: pd.DataFrame) -> pd.DataFrame:
        try:
            
            preprocessed_df = AutoClean(dataset, mode='auto')
            return preprocessed_df.output
        except Exception as e:
            return str(e)

class ScaleDataService:
    def __init__(self, method: str) -> None:
        self.method = method
        self.scaling_method = self.scaling_method

    def scaling_method(self):
        if self.method == 'standard':
            return StandardScaler()
        elif self.method == 'minmax':
            return MinMaxScaler()
        else:
            return None

    def process(self, dataset: pd.DataFrame) -> pd.DataFrame:
        try:            
            df = dataset
            if self.scaling_method != None:
                numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
                scaled_df = df.copy()
                scaled_df[numeric_columns] = pd.DataFrame(self.scaling_method.fit_transform(df[numeric_columns]), columns=numeric_columns)            
            else:
                return None
            return scaled_df
        except Exception as e:
            return str(e)