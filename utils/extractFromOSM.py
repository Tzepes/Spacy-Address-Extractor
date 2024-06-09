import osmium
import pandas as pd
import logging
import random

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# List of potential noise texts
noise_texts = [
    "Find us at:",
    "Visit our location at:",
    "You can locate us at:",
    "Our address is:",
    "We are situated at:",
    "Come see us at:",
    "Located at:",
    "Reach us at:",
    "Our office is at:",
    "Address:"
]

# List of Australian regions
australian_regions = [
    "New South Wales", "NSW", "Victoria", "VIC", "Queensland", "QLD",
    "South Australia", "SA", "Western Australia", "WA", "Tasmania", "TAS",
    "Northern Territory", "NT", "Australian Capital Territory", "ACT"
]

class AddressHandler(osmium.SimpleHandler):
    def __init__(self, num_addresses, log_interval=1000):
        osmium.SimpleHandler.__init__(self)
        self.num_addresses = num_addresses
        self.processed_count = 0
        self.log_interval = log_interval
        self.file_initialized = False
        self.addresses = []
        self.selected_regions = australian_regions  # Randomly select regions

    def node(self, n):
        try:
            if len(self.addresses) >= self.num_addresses:
                return
            addr_housenumber = n.tags.get('addr:housenumber')
            addr_street = n.tags.get('addr:street')
            addr_city = n.tags.get('addr:city')
            addr_postcode = n.tags.get('addr:postcode')
            addr_state = n.tags.get('addr:state')
            addr_country = 'Australia'

            if addr_state not in self.selected_regions:
                return

            if addr_housenumber and addr_street and addr_city and addr_postcode:
                # Check for postal boxes
                if 'PO Box' in addr_housenumber:
                    postal_box = addr_housenumber
                    street_address = f"{postal_box}, {addr_city} {addr_postcode}"
                else:
                    street_address = f"{addr_housenumber} {addr_street}"

                noise_text = random.choice(noise_texts)
                full_text = f"{noise_text} {street_address}, {addr_city} {addr_postcode}" if random.random() > 0.5 else f"{street_address}, {addr_city} {addr_postcode}"
                
                address = {
                    'Text': full_text,
                    'Street_Number': addr_housenumber,
                    'Street_Name': addr_street,
                    'Street_Address': street_address,
                    'City': addr_city,
                    'Zip_Code': addr_postcode,
                    'State': addr_state if addr_state else '',
                    'Country': addr_country
                }
                self.addresses.append(address)
                self.append_to_csv(address)
                self.processed_count += 1
                # logging.info(f"Processed address: {address}")

            if self.processed_count % self.log_interval == 0:
                logging.info(f"Processed {self.processed_count} nodes. Collected {len(self.addresses)} addresses so far.")

        except Exception as e:
            logging.error(f"Error processing node {n.id}: {e}")

    def append_to_csv(self, address):
        df = pd.DataFrame([address])
        df['Address'] = df['Street_Address'] + ", " + df['City'] + " " + df['Zip_Code']
        df = df[['Text', 'Address', 'Street_Number', 'Street_Name', 'Street_Address', 'City', 'Zip_Code', 'State', 'Country']]
        mode = 'a' if self.file_initialized else 'w'
        header = not self.file_initialized
        df.to_csv('australian_addresses.csv', mode=mode, header=header, index=False)
        self.file_initialized = True

def extract_addresses(osm_file, num_addresses):
    handler = AddressHandler(num_addresses)
    logging.info(f"Starting address extraction from {osm_file}")
    logging.info(f"Selected regions for extraction: {handler.selected_regions}")
    
    try:
        handler.apply_file(osm_file)
    except Exception as e:
        logging.error(f"Error applying file: {e}")

    logging.info(f"Extracted {len(handler.addresses)} addresses")

# Example usage
osm_file = 'australia-latest.osm.pbf'
num_addresses = 5000  # Specify the number of addresses you want to extract
extract_addresses(osm_file, num_addresses)
