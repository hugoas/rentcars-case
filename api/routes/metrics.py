from fastapi import APIRouter, Depends
from api.services.data_service import read_events
from api.security import verify_api_key

router = APIRouter()

@router.get("/metrics/funnel", dependencies=[Depends(verify_api_key)])
def get_funnel():
    df = read_events()

    return {
        "total_events": int(df["count"].sum())
    }