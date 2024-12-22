from fastapi import APIRouter, HTTPException, Cookie
from src.services.DetectEmotion import detect_emotion
from pydantic import BaseModel
from src.routers.users import get_user_data  # get_user_data 메소드를 가져옵니다.

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
async def detect_emotion_user(request: ImagePathRequest, token: str = Cookie(None)):
    try:
        user = await get_user_data(token)
        
        # 사용자의 dominant emotion 판단
        dominant_emotion = await detect_emotion(request.img_path)
        
        user.emotion = dominant_emotion
        
        return {"emotion": dominant_emotion}
    
    except HTTPException as e:
            raise e  # get_user_data에서 발생한 HTTPException을 그대로 전달