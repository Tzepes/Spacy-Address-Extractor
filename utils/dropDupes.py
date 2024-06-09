import pandas as pd

# Load the dataset
df = pd.read_csv('datasets/randomized_de_address_dataset_no_dupes.csv')

# Drop duplicates based on 'Text' column
df = df.drop_duplicates(subset='Text')

# Save the dataframe to a new csv file
df.to_csv('datasets/randomized_de_address_dataset_no_dupes.csv', index=False)