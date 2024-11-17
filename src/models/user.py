from pydantic import BaseModel

class User(BaseModel):
    emotion: str
    playlist: str