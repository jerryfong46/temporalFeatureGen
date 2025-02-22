import click
import pandas as pd
from .transformer import TemporalTransformer

@click.command()
@click.argument('input_file')
@click.argument('output_file')
@click.option('--date-col', required=True, help='Name of the date column')
@click.option('--entity-col', required=True, help='Name of the entity column')
@click.option('--value-cols', required=True, help='Comma-separated list of value columns')
@click.option('--windows', default='7,30', help='Comma-separated list of window sizes in days')
@click.option('--aggregations', default='mean,std', help='Comma-separated list of aggregation functions')
def main(input_file, output_file, date_col, entity_col, value_cols, windows, aggregations):
    """Generate temporal features from input data"""
    
    # Load data
    df = pd.read_csv(input_file)
    
    # Parse parameters
    value_cols = value_cols.split(',')
    windows = [int(w) for w in windows.split(',')]
    aggregations = aggregations.split(',')
    
    # Create transformer
    transformer = TemporalTransformer(
        date_column=date_col,
        entity_column=entity_col,
        value_columns=value_cols
    )
    
    # Generate features
    result = transformer.add_window_features(
        df=df,
        windows=windows,
        aggregations=aggregations
    )
    
    # Save results
    result.to_csv(output_file, index=False) 