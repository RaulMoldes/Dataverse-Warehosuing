import pyspark.sql.functions as F   

def coalesce_column(df, column_name, invalid_values, coalesced_value=None):
    '''
    Function to coalesce values in a column based on a list of invalid values.
    
    :param df: PySpark DataFrame
    :param column_name: Column name to be checked
    :param invalid_values: List of values to treat as invalid (will be replaced with None)
    :param coalesced_value: Optional: Default value to use if column is None after coalescing
    :return: DataFrame with the coalesced column
    '''
    
    # Create a condition to check if the column value is in invalid_values
    condition = F.lit(False)  # Start with a False condition
    
    for value in invalid_values:
        # Add conditions for each invalid value (it could be a string or number)
        condition |= (F.trim(F.col(column_name)) == str(value))  # Convert to string for comparison
    
    # Coalesce column based on the condition
    df = df.withColumn(
        column_name,
        F.coalesce(
            F.when(condition, F.lit(None)).otherwise(F.col(column_name)),
            F.lit(coalesced_value)
        )
    )
    
    return df


def remove_columns(df, column_names: list):
  '''Function to remove columns from a pyspark dataframe'''
  for column_name in column_names:
    df = df.drop(column_name)
  return df

def set_min_value(df, column_name, min_value):
  '''Function to set the minimum value of a given string column on a pyspark dataframe'''
  df = df.withColumn(column_name, F.when(F.col(column_name) < min_value, F.lit(min_value)).otherwise(F.col(column_name)))
  return df

def set_max_value(df, column_name, max_value):
  '''Function to set the maximum value of a given string column on a pyspark dataframe'''
  df = df.withColumn(column_name, F.when(F.col(column_name) > max_value, F.lit(max_value)).otherwise(F.col(column_name)))
  return df

