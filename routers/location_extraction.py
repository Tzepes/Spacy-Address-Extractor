from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import spacy
from utils.similarityScoring import sort_companies_and_locations
from urllib.parse import urlparse


router = APIRouter()

# Define data models for incoming requests
class TextRequest(BaseModel):
    text: str
    domain: Optional[str] = None

# Load the pre-trained model for GPE and ORG extraction
nlp_gpe_org = spacy.load('en_core_web_trf')

# todo: IF BIG COMPANY LIKE GOOGLE, FACEBOOK ETC. IGNORE THE GPE AND ORG EXTRACTION

@router.post("/extract_gpe_org/")
async def extract_gpe_org(request: TextRequest):
    doc = nlp_gpe_org(request.text)

    gpe = []
    org = []
    sorted_ORGs_GPEs = []

    for entity in doc.ents:
        if entity.label_ == 'GPE':
            gpe.append(entity.text)
        elif entity.label_ == 'ORG':
            org.append(entity.text)

    if request.domain:
        domain = urlparse(request.domain).netloc
        sorted_ORGs_GPEs = sort_companies_and_locations(domain, org, gpe)
        return {"GPE": gpe, "ORG": org, "ORG_GPE_Sorted": sorted_ORGs_GPEs}
    else:
        return {"GPE": gpe, "ORG": org}