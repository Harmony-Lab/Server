from fastapi import APIRouter, HTTPException, Header
from src.services.spotify import create_playlist  # Spotify 서비스에서 생성한 함수 가져오기
from src.models.playlist import Playlist
from src.routers.users import get_user_data  # get_user_data 메소드를 가져옵니다.

router = APIRouter()
PLAYLIST_SIZE = 5

@router.post("/", response_model=Playlist)
async def create_user_playlist(authorization: str = Header(None)):
    # 사용자의 Playlist 생성
    try:
        # Authorization 헤더에서 JWT 토큰 추출
        jwtToken = authorization.split(" ")[1] if authorization else None
        user = await get_user_data(jwtToken)
        
        playlist = create_playlist(user.emotion, PLAYLIST_SIZE)
        
        user.playlist = playlist
        
        return playlist
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
