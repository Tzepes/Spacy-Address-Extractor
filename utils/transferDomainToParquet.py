import pandas as pd

# Read the CSV file
df = pd.read_csv('datasets/reatemptDomain.csv')

# Check if 'Domain' column exists in the DataFrame
if 'Domain' in df.columns:
    # Create a new DataFrame with only the 'Domain' column and rename it to 'domain'
    domain_df = df[['Domain']].rename(columns={'Domain': 'domain'}).drop_duplicates()

    # Write the new DataFrame to a Parquet file
    domain_df.to_parquet('falseResultedLinks.parquet', index=False)
else:
    print("Column 'Domain' does not exist in the DataFrame.")