import pandas as pd

# Read the CSV file
df = pd.read_csv('resultsToTemper.csv')

# Check if 'Domain' column exists in the DataFrame
if 'Domain' in df.columns:
    # Drop duplicates in the 'Domain' column
    df.drop_duplicates(subset='Domain', keep='first', inplace=True)

    # Write the DataFrame back to the CSV file
    df.to_csv('resultsToTemper.csv', index=False)
else:
    print("Column 'Domain' does not exist in the DataFrame.")