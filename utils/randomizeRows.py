import pandas as pd
import random
import csv

# Load the data from the CSV file
df = pd.read_csv('datasets/german_addressData.csv',  quoting=csv.QUOTE_ALL)

# Randomize the rows
df = df.sample(frac=1, random_state=random.randint(0, 511))

# Write the randomized data to a new CSV file
df.to_csv('datasets/randomized_de_address_dataset.csv', index=False, quoting=csv.QUOTE_ALL)