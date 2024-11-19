from pydantic import BaseModel, HttpUrl

class Song(BaseModel):
    title: str  # 제목
    artist: str  # 가수
    url: HttpUrl  # URL