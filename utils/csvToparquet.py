import pandas as pd

# Read the CSV file
df = pd.read_csv('C:/Users/andre/Downloads/domains.csv')

# Save as a Parquet file
df.to_parquet('./domainsToRetry.parquet', engine='pyarrow', index=False)
