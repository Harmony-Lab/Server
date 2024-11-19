from typing import Optional
from pydantic import BaseModel
from src.models.emotion import Emotion
from src.models.playlist import Playlist

class User(BaseModel):
    emotion: Optional[Emotion] = None
    playlist: Optional[Playlist] = None