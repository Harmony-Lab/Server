from pydantic import BaseModel, Field
from typing import List
from src.models.song import Song

class Playlist(BaseModel):
    songs: List[Song] = Field(default_factory=list, max_items=5)  # 최대 5개의 Song을 가질 수 있도록 설정
