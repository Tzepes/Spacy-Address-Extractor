from fastapi import FastAPI
from routers import address_extraction, location_extraction

app = FastAPI(title="NLP Extraction API")

# Include routers
app.include_router(address_extraction.router, prefix="/addresses", tags=["Addresses"])
app.include_router(location_extraction.router, prefix="/location", tags=["Location"])
