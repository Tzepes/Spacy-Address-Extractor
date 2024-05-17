import pandas as pd

# # Read the CSV file into a DataFrame
# df = pd.read_csv('./addressParser_sawpnil_Data/us-train-dataset.csv')

# def drop_column(df, column_name):
#     '''Drop a column from a DataFrame'''
#     return df.drop(column_name, axis=1)

# def switch_columns(df):
#     '''Switch the positions of two columns in a DataFrame'''
#     columns_reordered = ['Text', 'Address', 'Street_Number', 'Street_Name', 'Street_Address', 'City', 'Zip_Code', 'State', 'Country']
#     df = df.reindex(columns=columns_reordered)
#     return df 
# # Drop the 'Building_Name' column
# # drop_column(df, 'Building_Name')

# # Create the 'Street_Address' column
# df['Street_Address'] = df['Street_Number'].astype(str) + ' ' + df['Street_Name']

# # Create the 'Text' column
# df['Text'] = df['Address']

# # Reorder the columns
# df = switch_columns(df)

# # Write the DataFrame back to a CSV file
# df.to_csv('us-train-dataset.csv', index=False)
# df['Text'].to_csv('text-only.csv', index=False)

# # Read the CSV files into separate DataFrames
# df1 = pd.read_csv('changeText.csv')
# df2 = pd.read_csv('text-only.csv')

# # Replace the 'Text' column in df1 with the 'Text' column from df2
# df1['Text'] = df2['Text']
# print(df1)
# print(df2)
# # Write the modified DataFrame back to a CSV file
# df1.to_csv('changeText.csv', index=False)

# # Read the CSV file into a DataFrame
# df = pd.read_csv('extended_data.csv')

# # Select the 'Text' column, enclose each entry in quotes, add a comma at the end, and write it to a text file
# with open('text-only.txt', 'w') as f:
#     for text in df['Text']:
#         f.write(f'"{text}",\n')

# # Write all rows and columns to a text file, with each entry enclosed in quotes and followed by a comma
# with open('text_address_data.txt', 'w') as f:
#     for _, row in df[['Text', 'Address']].iterrows():
#         f.write(f'"{row["Text"] if pd.notna(row["Text"]) else ""}|{row["Address"] if pd.notna(row["Address"]) else ""}",\n')

# Read the CSV files into separate DataFrames
df_extended = pd.read_csv('extended_data.csv')
df_noise = pd.read_csv('text_noise_address.csv', on_bad_lines='skip')

# Add the 'Noise' column from df_noise to df_extended
df_extended['Noise'] = df_noise['Noise']

# Fill in missing values in the 'Noise' column with a default value
df_extended['Noise'] = df_extended['Noise'].fillna('')

# Write the modified DataFrame back to a CSV file
df_extended.to_csv('extended_data.csv', index=False)