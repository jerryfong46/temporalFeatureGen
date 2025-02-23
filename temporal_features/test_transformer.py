import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from temporal_features.transformer import TemporalTransformer

def generate_dummy_data(start_date: str = '2023-01-01', periods: int = 100) -> pd.DataFrame:
    """Generate dummy data for testing"""
    # Create date range
    dates = pd.date_range(start=start_date, periods=periods, freq='D')
    
    # Create customer IDs and product IDs
    customer_ids = np.random.choice(['C1', 'C2', 'C3'], size=periods)
    product_ids = np.random.choice(['P1', 'P2'], size=periods)
    
    # Generate random sales and quantity data
    sales = np.random.uniform(10, 100, size=periods)
    quantity = np.random.randint(1, 10, size=periods)
    
    # Create DataFrame
    df = pd.DataFrame({
        'date': dates,
        'customer_id': customer_ids,
        'product_id': product_ids,
        'sales': sales,
        'quantity': quantity
    })
    
    return df

def test_temporal_transformer():
    """Test the TemporalTransformer with multiple entity levels"""
    # Generate dummy data
    df = generate_dummy_data()
    
    # Initialize transformer with multiple entity levels
    transformer = TemporalTransformer(
        date_column='date',
        entity_columns=['customer_id', 'product_id'],
        value_columns=['sales', 'quantity']
    )
    
    # Add window features
    result_df = transformer.add_window_features(
        df=df,
        windows=[7, 14],  # 7-day and 14-day windows
        aggregations=['mean', 'std']
    )
    
    # Print sample results
    print("\nInput DataFrame Sample:")
    print(df.head())
    print("\nOutput DataFrame Sample:")
    print(result_df.head())
    
    # Verify the new columns
    new_columns = [col for col in result_df.columns if col not in df.columns]
    print("\nNew Feature Columns:")
    for col in new_columns:
        print(f"- {col}")
    
    # Basic assertions
    assert len(result_df) == len(df), "Row count should remain the same"
    assert len(new_columns) == 16, "Should have 16 new features (2 values × 2 windows × 2 aggs × 2 entity levels)"
    
    return result_df

if __name__ == "__main__":
    result = test_temporal_transformer() 