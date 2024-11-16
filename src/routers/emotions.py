from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.models.emotion import Emotion
from src.DetectEmotion import BasetoImage, GetEmotionProbsDeepFace, GetEmotionProbsFER, MergeEmotionProbs
from pydantic import BaseModel

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
async def detect_emotion(request: ImagePathRequest):
    # Base64 데이터 이미지 변환
    img = BasetoImage(base64_data=request.img_path)
    
    # DeepFace와 FER로 감정 확률 분석
    deepface_probs = GetEmotionProbsDeepFace(img)
    fer_probs = GetEmotionProbsFER(img)

    # 두 모델의 결과를 결합
    dominant_emotion, combined_probs = MergeEmotionProbs(deepface_probs, fer_probs)

    return JSONResponse(content={"emotion": dominant_emotion})
