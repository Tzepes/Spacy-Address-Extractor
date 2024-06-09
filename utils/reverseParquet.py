import pandas as pd

# Load the .parquet file into a DataFrame
df = pd.read_parquet('websitesFiltered.snappy.parquet')

# Reverse the order of the rows
df = df.iloc[::-1]

# Save the DataFrame back to a .parquet file
df.to_parquet('websitesFilteredReversed.snappy.parquet')