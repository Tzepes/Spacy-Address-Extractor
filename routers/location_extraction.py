from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import spacy
from langdetect import detect
from utils.similarityScoring import sort_companies_and_locations
from urllib.parse import urlparse


router = APIRouter() 

# Define data models for incoming requests
class TextRequest(BaseModel):
    text: str
    domain: Optional[str] = None

model_map = {
    'en': 'en_core_web_trf',
    'de': 'de_core_news_lg',
}

# todo: IF BIG COMPANY LIKE GOOGLE, FACEBOOK ETC. IGNORE THE GPE AND ORG EXTRACTION

@router.post("/extract_gpe_org/")
async def extract_gpe_org(request: TextRequest):
    # Detect the language of the text
    lang = detect(request.text)
    print(lang)
    nlp_gpe_org = spacy.load(model_map.get(lang, 'en_core_web_trf'))

    doc = nlp_gpe_org(request.text)
    print(doc.ents)
    gpe = []
    org = []
    sorted_ORGs_GPEs = []
    for entity in doc.ents:
        if entity.label_ == 'GPE' or entity.label_ == 'LOC':
            gpe.append(entity.text)
        elif entity.label_ == 'ORG':
            org.append(entity.text)

    if request.domain and org:
        domain = urlparse(request.domain).netloc
        sorted_ORGs_GPEs, org, gpe = sort_companies_and_locations(domain, org, gpe)
        print({"GPE": gpe, "ORG": org, "ORG_GPE_Sorted": sorted_ORGs_GPEs, "language": lang})
        return {"GPE": gpe, "ORG": org, "ORG_GPE_Sorted": sorted_ORGs_GPEs, "language": lang}
    else:
        print({"GPE": gpe, "ORG": org, "ORG_GPE_Sorted": sorted_ORGs_GPEs, "language": lang})
        return {"GPE": gpe, "ORG": org, "ORG_GPE_Sorted": sorted_ORGs_GPEs, "language": lang}