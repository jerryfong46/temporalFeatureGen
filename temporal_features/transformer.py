from typing import List, Union, Callable, Dict
import pandas as pd
import numpy as np

class TemporalTransformer:
    """Main class for generating temporal features"""
    
    def __init__(self, 
                 date_column: str,
                 entity_columns: Union[str, List[str]],  # Changed to support single string or list
                 value_columns: List[str]):
        self.date_column = date_column
        # Convert single string to list for consistency
        self.entity_columns = [entity_columns] if isinstance(entity_columns, str) else entity_columns
        self.value_columns = value_columns
        
    def add_window_features(self,
                          df: pd.DataFrame,
                          windows: List[int],
                          aggregations: List[str] = ['mean', 'std']) -> pd.DataFrame:
        """
        Generate temporal features for specified windows at multiple entity levels
        
        Args:
            df: Input DataFrame
            windows: List of window sizes in days
            aggregations: List of aggregation functions to apply
            
        Returns:
            DataFrame with additional temporal features
        """
        df = df.copy()
        df[self.date_column] = pd.to_datetime(df[self.date_column])
        
        # ------------------------------------------------
        # Sort the DataFrame by all grouping columns + date
        # ------------------------------------------------
        df = df.sort_values(by=self.entity_columns + [self.date_column])
        
        # Generate features for each combination of entity levels
        for i in range(1, len(self.entity_columns) + 1):
            # Get all combinations of entity columns up to length i
            entity_group = self.entity_columns[:i]
            group_suffix = '_'.join(col.lower() for col in entity_group)
            
            for window in windows:
                for col in self.value_columns:
                    for agg in aggregations:
                        feature_name = f"{col}_{window}d_{agg}_{group_suffix}"
                        df[feature_name] = (
                            df.groupby(entity_group)
                            [col]
                            .rolling(window=f"{window}D", on=self.date_column)
                            .agg(agg)
                            .reset_index(level=list(range(len(entity_group))), drop=True)
                        )
        
        return df 