from fastapi import APIRouter
from pydantic import BaseModel
import spacy

router = APIRouter()

# Define data models for incoming requests
class TextRequest(BaseModel):
    text: str

# Load the pre-trained model for GPE and ORG extraction
nlp_gpe_org = spacy.load('en_core_web_trf')

# todo: IF BIG COMPANY LIKE GOOGLE, FACEBOOK ETC. IGNORE THE GPE AND ORG EXTRACTION

@router.post("/extract_gpe_org/")
async def extract_gpe_org(request: TextRequest):
    doc = nlp_gpe_org(request.text)
    gpe = [entity.text for entity in doc.ents if entity.label_ == 'GPE']
    org = [entity.text for entity in doc.ents if entity.label_ == 'ORG']
    print(gpe)
    print(org)
    return {"GPE": gpe, "ORG": org}