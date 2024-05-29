import spacy

nlp=spacy.load("output/models_de/model-best")

address="Our Site is operated by TidyWare UK Ltd, a company registered in England and Wales under number 06831241, whose registered office is at TidyWare UK Ltd, Edwinstowe House, Centre For Business Excellence, Edwinstowe NG21 9PR"
doc=nlp(address)
ent_list=[(ent.text, ent.label_) for ent in doc.ents]
# print("Address string -> "+address)
# print("Parsed address -> "+str(ent_list))

# # Loading Entity Ruler coupled NER model and checking prediction
nlp=spacy.load("output/models_uk/model-best")

doc=nlp(address)

# Create separate lists for the text and labels
ent_text = [ent.text for ent in doc.ents]
ent_labels = [ent.label_ for ent in doc.ents]

ent_list=[(ent.text, ent.label_) for ent in doc.ents]
print("Address string -> "+address)
print("Parsed address -> "+str(ent_list))

for ent in doc.ents:
    print(f"'{ent.text}', '{ent.label_}'")

class StreetAddress:
    def __init__(self, street_name=None, street_num=None):
        self.street_name = street_name
        self.street_num = street_num

def parse_address(text):
    doc = nlp(text)
    ent_list = [(ent.text, ent.label_) for ent in doc.ents]
    street_name = None
    street_num = None
    for ent_text, ent_label in ent_list:
        if ent_label == 'STREET_NAME' and not street_name:
            street_name = ent_text
        elif ent_label == 'STREET_NUM' and not street_num:
            street_num = ent_text
        if street_name and street_num:
            break
    return StreetAddress(street_name, street_num)

