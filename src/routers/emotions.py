from fastapi import APIRouter, Cookie, HTTPException
from fastapi.responses import JSONResponse
from src.models.emotion import Emotion
from src.models.user import User
from src.DetectEmotion import BasetoImage, GetEmotionProbsDeepFace, GetEmotionProbsFER, MergeEmotionProbs
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
async def detect_emotion(request: ImagePathRequest, session_id: str = Cookie(None)):
    # 사용자 데이터 조회
    user_data = await get_user(session_id)
    
    # Base64 데이터 이미지 변환
    img = BasetoImage(base64_data=request.img_path)
    
    # DeepFace와 FER로 감정 확률 분석
    deepface_probs = GetEmotionProbsDeepFace(img)
    fer_probs = GetEmotionProbsFER(img)

    # 두 모델의 결과를 결합
    dominant_emotion, combined_probs = MergeEmotionProbs(deepface_probs, fer_probs)
    user_data.emotion = Emotion(emotion=dominant_emotion)
    return {"emotion": user_data.emotion}
