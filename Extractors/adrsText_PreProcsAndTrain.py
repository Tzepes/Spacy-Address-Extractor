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

def create_entity_spans(df):
    '''Create entity spans for training/test datasets'''
    df['Address'] = df['Address'].apply(lambda x: cleanup_data(x))
    df['EntitySpans'] = df.apply(lambda row: (row['Text'], get_address_span(row['Text'], row['Address'])), axis=1)
    return df['EntitySpans']

def get_address_span(text, address):
    '''Find the start and end indices of the address in the text'''
    start = text.find(address)
    end = start + len(address)
    return [(start, end, 'Address')] if start != -1 else []

def get_doc_bin(training_data, nlp):
    '''Create DocBin object for building training/test corpus'''
    db = DocBin()
    for text, annotations in training_data:
        doc = nlp(text)  # Construct a Doc object
        ents = []
        for start, end, label in annotations:
            span = doc.char_span(start, end, label=label)
            if span:
                ents.append(span)
        doc.ents = ents
        db.add(doc)
    return db

#Load blank English model. This is needed for initializing a Document object for our training/test set.
nlp = spacy.blank("en")

# Read the entire dataset into pandas
try:
    df = pd.read_csv(filepath_or_buffer="datasets/text_address.csv", sep=",", dtype=str, on_bad_lines='skip')
except pd.errors.ParserError as e:
    print(f"Error parsing CSV: {e}")
    exit()

# Split the dataset into training (80%) and validation (20%)
df_train, df_test = train_test_split(df, test_size=0.2, random_state=42)

# Get entity spans for training dataset
df_entity_spans_train = create_entity_spans(df_train.astype(str))
training_data = df_entity_spans_train.values.tolist()

# Get entity spans for validation dataset
df_entity_spans_test = create_entity_spans(df_test.astype(str))
validation_data = df_entity_spans_test.values.tolist()

# Create the directory if it doesn't exist
if not os.path.exists("./corpus/spacy-docbins"):
    os.makedirs("./corpus/spacy-docbins")

# Get & Persist DocBin for training data
doc_bin_train = get_doc_bin(training_data, nlp)
doc_bin_train.to_disk("./corpus/spacy-docbins/trainText_Address.spacy")

# Get & Persist DocBin for validation data
doc_bin_test = get_doc_bin(validation_data, nlp)
doc_bin_test.to_disk("./corpus/spacy-docbins/testText_Address.spacy")