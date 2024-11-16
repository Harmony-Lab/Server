from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.models.emotion import Emotion
from src.DetectEmotion import GetDominantEmotion
from pydantic import BaseModel

router = APIRouter()

class ImagePathRequest(BaseModel):
    img_path: str

@router.post("/api/emotion", description= "감정 인식 결과 전달",
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
    dominant_emotion = GetDominantEmotion(src=request.img_path)
    return JSONResponse(content={"emotion": dominant_emotion})
