from fastapi import APIRouter, Cookie, HTTPException
from src.services.spotify import create_playlist  # Spotify 서비스에서 생성한 함수 가져오기
from src.routers.users import get_user
from src.models.playlist import Playlist

router = APIRouter()
PLAYLIST_SIZE = 5

@router.post("/api/playlists/", response_model=Playlist)
async def create_user_playlist(session_id: str = Cookie(None)):
    # 사용자 데이터 조회
    user_data = await get_user(session_id)
    
    # 사용자의 Playlist 생성
    try:
        playlist = create_playlist(user_data.emotion.emotion, PLAYLIST_SIZE)
        user_data.playlist = playlist
        return playlist
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while creating the playlist.")
