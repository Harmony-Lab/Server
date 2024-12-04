from fastapi import APIRouter
from src.services.DetectEmotion import detect_emotion
from pydantic import BaseModel

router = APIRouter()

class ImagePathRequest(BaseModel):
    img_path: str

@router.post("/", description= "감정 인식 결과 전달",
        responses={
            200: {
                "content": {
                "application/json": {
                    "example": {
                        "emotion": "dominant_emotion"}
                }
            }
            }
        })
async def detect_emotion_user(request: ImagePathRequest):
    # 사용자의 emotion 판단
    dominant_emotion = await detect_emotion(request.img_path)
    return {"emotion": dominant_emotion}
