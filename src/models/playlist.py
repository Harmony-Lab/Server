from pydantic import BaseModel
from typing import List
from src.models.song import Song

class Playlist(BaseModel):
    size: int
    songs: List[Song]
