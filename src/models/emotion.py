from pydantic import BaseModel
from datetime import datetime

class Emotion(BaseModel):
    id: int
    user_id: int
    emotion: str
    timestamp: datetime
