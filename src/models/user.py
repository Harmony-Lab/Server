from pydantic import BaseModel
from src.models.emotion import Emotion

class User(BaseModel):
    emotion: Emotion
    playlist: str