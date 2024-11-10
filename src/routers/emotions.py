from fastapi import APIRouter
from src.models.emotion import Emotion

router = APIRouter()

'''
@router.get("/api/test/")
async def create_item_draft():
    return {"emotion": "happy"}
'''

@router.post("/api/emotions/")
async def create_item(emotion: Emotion):
    return {"emotion": emotion}
