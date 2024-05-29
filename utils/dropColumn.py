import pandas as pd

# Load the CSV file
df = pd.read_csv('datasets/randomized_uk_address_dataset.csv')

# Drop the 'B-zipcode' and 'I-Zipcode' columns
df = df.drop(['B-Zipcode', 'I-Zipcode'], axis=1)

# Save the DataFrame back to CSV
df.to_csv('datasets/DRP_randomized_uk_address_dataset.csv', index=False)