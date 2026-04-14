from fastapi import APIRouter

router = APIRouter()

@router.post("/events/ingest")
def ingest_event(event: dict):
    return {"message": "received"}