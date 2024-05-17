import spacy

nlp = spacy.load('en_core_web_trf')

text = "Profile Howe Drafting Services are one of Sydney's premier drafting and design companies. The company works with various leading architects and consulting engineers in and around Sydney on a range of important civil and structural works associated with significant projects. We continue to be engaged by both public, governmental departments and leading engineering firms - a testament to our dedication to quality drafting design and delivery. It's because of this that our customers consistently receive the utmost service in both professionalism and quality."  

doc = nlp(text)

print("GPEs ____________________________________________________________")
for entity in doc.ents:
   if entity.label_ == 'GPE':
      print(entity.text)

print("")
print("ORGs ____________________________________________________________")

for entity in doc.ents:
   if entity.label_ == 'ORG':
      print(entity.text)