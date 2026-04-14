from fastapi import APIRouter

router = APIRouter()

@router.get("/partners/{partner_id}")
def get_partner(partner_id: int):
    return {"partner_id": partner_id}