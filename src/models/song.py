from pydantic import BaseModel

class Song(BaseModel):
    title: str  # 제목
    artist: str  # 가수
    url: str  # URL