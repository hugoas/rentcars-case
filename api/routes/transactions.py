from fastapi import APIRouter

router = APIRouter()

@router.get("/transactions/summary")
def get_summary():
    return {"status": "ok"}