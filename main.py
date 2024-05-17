from fastapi import FastAPI
from routers.address_extraction import router as street_router
from routers.location_extraction import router as gpe_org_router

app = FastAPI()

# Include routers
app.include_router(street_router)
app.include_router(gpe_org_router)
