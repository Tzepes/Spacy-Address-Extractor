import pandas as pd
import random

# Load the data from the CSV file
df = pd.read_csv('datasets/extended_data.csv')

# Randomize the rows
df = df.sample(frac=1, random_state=random.randint(0, 100))

# Write the randomized data to a new CSV file
df.to_csv('datasets/randomized_us_address_dataset.csv', index=False)