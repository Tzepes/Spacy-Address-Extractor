#This script takes the data from a CSV file, preprocesses it and trains a model to extract addresses from the text.
import os
import spacy
from spacy.tokens import DocBin
import pandas as pd
import re
pd.set_option('display.max_colwidth', None)
from sklearn.model_selection import train_test_split

def cleanup_data(address):
    '''Pre process address string to remove new line characters, add comma punctuations etc.'''
    cleansed_address1=re.sub(r'(,)(?!\s)',', ',address)
    cleansed_address2=re.sub(r'(\\n)',', ',cleansed_address1)
    cleansed_address3=re.sub(r'(?!\s)(-)(?!\s)',' - ',cleansed_address2)
    cleansed_address=re.sub(r'\.','',cleansed_address3)
    return cleansed_address

def get_address_span(address=None, address_component=None, label=None):
    '''Search for specified address component and get the span.'''
    if pd.isna(address_component) or str(address_component) == 'nan':
        return None
    address_component1 = re.sub(r'\.', '', address_component)
    address_component2 = re.sub(r'(?!\s)(-)(?!\s)', ' - ', address_component1)
    span = re.search(r'\b(?:' + re.escape(address_component2) + r')\b', address)
    if span:
        return (span.start(), span.end(), label)
    return None

    
def extend_list(entity_list,entity):
    if pd.isna(entity):
        return entity_list
    else:
        entity_list.append(entity)
        return entity_list

def create_entity_spans(df,tag_list):
    '''Create entity spans for training/test datasets'''
    df['Address'] = df['Address'].apply(lambda x: cleanup_data(x))
    df["StreetNumber"] = df.apply(lambda row: get_address_span(address=row['Address'], address_component=row['Street_Number'], label='STREET_NUM'), axis=1)
    df["StreetNameTag"] = df.apply(lambda row: get_address_span(address=row['Address'], address_component=row['Street_Name'], label='STREET_NAME'), axis=1)
    df["CityTag"] = df.apply(lambda row: get_address_span(address=row['Address'], address_component=row['City'], label='CITY'), axis=1)
    df["ZipCodeTag"] = df.apply(lambda row: get_address_span(address=row['Address'], address_component=row['Zip_Code'], label='ZIP_CODE'), axis=1)
    # df["BZipCodeTag"] = df.apply(lambda row: get_address_span(address=row['Address'], address_component=row['B-Zip_Code'], label='B-ZIP_CODE'), axis=1)
    # df["IZipCodeTag"] = df.apply(lambda row: get_address_span(address=row['Address'], address_component=row['I-Zip_Code'], label='I-ZIP_CODE'), axis=1)
    df["StateTag"] = df.apply(lambda row: get_address_span(address=row['Address'], address_component=row['State'], label='STATE'), axis=1)
    df["CountryTag"] = df.apply(lambda row: get_address_span(address=row['Address'], address_component=row['Country'], label='COUNTRY'), axis=1)
    df['EmptySpan'] = df.apply(lambda x: [], axis=1)

    for i in tag_list:
        df['EntitySpans']=df.apply(lambda row: extend_list(row['EmptySpan'],row[i]),axis=1)
        df['EntitySpans']=df[['EntitySpans','Address']].apply(lambda x: (x[1], x[0]),axis=1)
    return df['EntitySpans']

def get_doc_bin(training_data, nlp):
    '''Create DocBin object for building training/test corpus'''
    db = DocBin()
    for text, annotations in training_data:
        doc = nlp(text)  # Construct a Doc object
        ents = []
        valid_annotations = remove_overlapping_spans(annotations)  # Ensure no overlapping spans
        for start, end, label in valid_annotations:
            span = doc.char_span(start, end, label=label)
            if span:
                ents.append(span)
        doc.ents = ents
        db.add(doc)
    return db

def remove_overlapping_spans(spans):
    '''Remove overlapping spans from the list of spans.'''
    sorted_spans = sorted(spans, key=lambda x: x[0])
    non_overlapping_spans = []
    last_end = -1
    for start, end, label in sorted_spans:
        if start >= last_end:
            non_overlapping_spans.append((start, end, label))
            last_end = end
    return non_overlapping_spans


#Load blank English model. This is needed for initializing a Document object for our training/test set.
nlp = spacy.blank("en")

# Define custom entity tag list
tag_list = ["StreetNumber", "StreetNameTag", "ZipCodeTag", "CityTag", "StateTag", "CountryTag"]

# Read the entire dataset into pandas
try:
    df = pd.read_csv(filepath_or_buffer="datasets/australian_addresses.csv", sep=",", dtype=str, on_bad_lines='skip')
except pd.errors.ParserError as e:
    print(f"Error parsing CSV: {e}")
    exit()

# If 'Text' column is the same as 'Address', drop the 'Text' column
if 'Text' in df.columns and df['Text'].equals(df['Address']):
    df = df.drop(columns=['Text'])

# Split the dataset into training (80%) and validation (20%)
df_train, df_test = train_test_split(df, test_size=0.2, random_state=42)

# Get entity spans for training dataset
df_entity_spans_train = create_entity_spans(df_train.astype(str), tag_list)
training_data = df_entity_spans_train.values.tolist()

# Get entity spans for validation dataset
df_entity_spans_test = create_entity_spans(df_test.astype(str), tag_list)
validation_data = df_entity_spans_test.values.tolist()

# Create the directory if it doesn't exist
if not os.path.exists("./corpus/spacy-docbins"):
    os.makedirs("./corpus/spacy-docbins")

# Get & Persist DocBin for training data
doc_bin_train = get_doc_bin(training_data, nlp)
doc_bin_train.to_disk("./corpus/spacy-docbins/trainAU.spacy")

# Get & Persist DocBin for validation data
doc_bin_test = get_doc_bin(validation_data, nlp)
doc_bin_test.to_disk("./corpus/spacy-docbins/testAU.spacy")


#Define custom entity tag list
# tag_list=["BuildingTag","StreetNumber","RecipientTag","StreetNameTag","ZipCodeTag","CityTag","StateTag","CountryTag"]


# ###### Training dataset prep ###########
# # Read the training dataset into pandas
# df_train=pd.read_csv(filepath_or_buffer="./addressParser_sawpnil_Data/us-train-dataset.csv",sep=",",dtype=str)

# # Get entity spans
# df_entity_spans= create_entity_spans(df_train.astype(str),tag_list)
# training_data= df_entity_spans.values.tolist()

# # Create the directory if it doesn't exist
# if not os.path.exists("./corpus/spacy-docbins"):
#     os.makedirs("./corpus/spacy-docbins")

# # Get & Persist DocBin to disk
# doc_bin_train= get_doc_bin(training_data,nlp)
# doc_bin_train.to_disk("./corpus/spacy-docbins/train.spacy")
# ######################################

# ###### Validation dataset prep ###########
# # Read the validation dataset into pandas
# df_test=pd.read_csv(filepath_or_buffer="./addressParser_sawpnil_Data/us-test-dataset.csv",sep=",",dtype=str)

# # Get entity spans
# df_entity_spans= create_entity_spans(df_test.astype(str),tag_list)
# validation_data= df_entity_spans.values.tolist()

# # Get & Persist DocBin to disk
# doc_bin_test= get_doc_bin(validation_data,nlp)
# doc_bin_test.to_disk("./corpus/spacy-docbins/test.spacy")
##########################################