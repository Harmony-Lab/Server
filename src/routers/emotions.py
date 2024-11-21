from fastapi import APIRouter, Cookie
from src.models.emotion import Emotion
from src.DetectEmotion import detect_emotion
from pydantic import BaseModel
from src.routers.users import get_user

router = APIRouter()

class ImagePathRequest(BaseModel):
    img_path: str

@router.post("/api/emotions", description= "감정 인식 결과 전달",
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
async def detect_emotio_user(request: ImagePathRequest, session_id: str = Cookie(None)):
    # 사용자 데이터 조회
    user_data = await get_user(session_id)
    
    # 사용자의 emotion 판단
    dominant_emotion = await detect_emotion(request.img_path)
    
    # 사용자 emotion 정보 수정
    user_data.emotion = Emotion(emotion=dominant_emotion)
    return {"emotion": dominant_emotion}
