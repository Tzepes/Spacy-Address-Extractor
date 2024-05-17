from fastapi import APIRouter, HTTPException
from Extractors.adrsParser_Predict import parse_address  # Import the function

router = APIRouter()

@router.post("/extract/")
async def extract_address(sample: TextSample):
    addresses = parse_address(sample.text)  # Use the imported function
    if not addresses:
        raise HTTPException(status_code=404, detail="No addresses found.")
    return {"addresses": addresses}