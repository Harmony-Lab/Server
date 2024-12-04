from fastapi import APIRouter, HTTPException
from src.services.spotify import create_playlist  # Spotify 서비스에서 생성한 함수 가져오기
from src.models.emotion import Emotion
from src.models.playlist import Playlist

router = APIRouter()
PLAYLIST_SIZE = 5

@router.post("/", response_model=Playlist)
async def create_user_playlist(request: Emotion):
    # 사용자의 Playlist 생성
    try:
        playlist = create_playlist(request.emotion, PLAYLIST_SIZE)
        return playlist
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
