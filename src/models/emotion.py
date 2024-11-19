from pydantic import BaseModel
from typing import Literal

class Emotion(BaseModel):
    emotion: Literal[
        'sad', 'happy', 'energetic', 'calm', 'angry', 
        'fear', 'neutral', 'disgust', 'surprise'
    ]
