from typing import List, Union, Callable, Dict
import pandas as pd
import numpy as np

class TemporalTransformer:
    """Main class for generating temporal features"""
    
    def __init__(self, 
                 date_column: str,
                 entity_column: str,
                 value_columns: List[str]):
        self.date_column = date_column
        self.entity_column = entity_column
        self.value_columns = value_columns
        
    def add_window_features(self,
                          df: pd.DataFrame,
                          windows: List[int],
                          aggregations: List[str] = ['mean', 'std']) -> pd.DataFrame:
        """
        Generate temporal features for specified windows
        
        Args:
            df: Input DataFrame
            windows: List of window sizes in days
            aggregations: List of aggregation functions to apply
            
        Returns:
            DataFrame with additional temporal features
        """
        df = df.copy()
        df[self.date_column] = pd.to_datetime(df[self.date_column])
        
        for window in windows:
            for col in self.value_columns:
                for agg in aggregations:
                    feature_name = f"{col}_{window}d_{agg}"
                    df[feature_name] = (
                        df.groupby(self.entity_column)
                        [col]
                        .rolling(window=f"{window}D", on=self.date_column)
                        .agg(agg)
                        .reset_index(level=0, drop=True)
                    )
        
        return df 