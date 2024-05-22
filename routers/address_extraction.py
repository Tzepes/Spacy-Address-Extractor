from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import spacy

router = APIRouter()

class TextRequest(BaseModel):
    text: str

# Assuming you're running this from the root of your project where main.py is, adjust the path like this:
nlp_address = spacy.load("output/models/model-best")

@router.post("/extract_street/")
async def extract_street(request: TextRequest):
    print(request.text)
    doc = nlp_address(request.text)
    city = None
    state = None
    street_name = None
    street_num = None
    zipcode = None
    for ent in doc.ents:
        if ent.label_ == 'CITY':
            city = ent.text
        elif ent.label_ == 'STATE':
            state = ent.text
        elif ent.label_ == 'STREET_NAME':
            street_name = ent.text
        elif ent.label_ == 'STREET_NUM':
            street_num = ent.text
        elif ent.label_ == 'ZIP_CODE':
            zipcode = ent.text
    if street_name or street_num:
        print(city, state, street_name, street_num, zipcode)
        return {"City": city, "State": state, "Street_Name": street_name, "Street_Num": street_num, "Zipcode": zipcode}
    else:
        return {"detail": "No street address found"}
