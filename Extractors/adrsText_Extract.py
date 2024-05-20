import spacy

# Loading Entity Ruler coupled NER model and checking prediction
nlp=spacy.load("output/models/addressFromText/model-best")

address="Submit Thanks for submitting! Contact 2100 Palomar Airport Road 219, Carlsbad, CA, 92008 USA "
doc=nlp(address)

# Print all entities
for ent in doc.ents:
    print(f"'{ent.text}', '{ent.label_}'")

