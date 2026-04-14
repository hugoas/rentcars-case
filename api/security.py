from fastapi import Header, HTTPException
from typing import Optional

API_KEY = "rentcars-secret"

def verify_api_key(x_api_key: Optional[str] = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")