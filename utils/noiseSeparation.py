import pandas as pd

def extract_noise(text, address, country):
    """
    Function to extract non-address and non-country parts from the text.
    """
    # Normalize text to avoid mismatches due to case sensitivity or trailing spaces
    text_normalized = " ".join(text.split()).lower()
    address_normalized = " ".join(address.split()).lower()
    country_normalized = country.lower() if pd.notna(country) else ''

    # Remove the address and country parts from the text
    noise = text_normalized.replace(address_normalized, "").replace(country_normalized, "").strip()

    # Replace multiple spaces with a single space
    noise = " ".join(noise.split())
    return noise

def process_csv(input_file_path, output_file_path):
    """
    Load CSV, process data to extract noise, and save to new CSV.
    """
    # Load the data from the CSV file using on_bad_lines='skip' to handle malformed lines
    data = pd.read_csv(input_file_path, on_bad_lines='skip')

    # Create the 'Noise' column
    data['Noise'] = data.apply(lambda row: extract_noise(row['Text'], row['Address'], row['Country']), axis=1)

    # Save the updated DataFrame to a new CSV file
    data.to_csv(output_file_path, index=False)
    print(f"Updated data saved to {output_file_path}")

input_file_path = 'extended_data.csv'
output_file_path = 'extended_dataWNoise.csv'

# Process the CSV
process_csv(input_file_path, output_file_path)
