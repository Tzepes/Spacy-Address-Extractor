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
    doc = nlp_address(request.text)
    street_name = None
    street_num = None
    for ent in doc.ents:
        if ent.label_ == 'STREET_NAME':
            street_name = ent.text
        elif ent.label_ == 'STREET_NUM':
            street_num = ent.text
    if street_name or street_num:
        return {"Street_Name": street_name, "Street_Num": street_num}
    else:
        raise HTTPException(status_code=404, detail="No street details found")
