from fastapi import APIRouter, HTTPException, Response, Cookie
from src.models.user import User
from src.models.emotion import Emotion
from typing import Optional
from uuid import uuid4

router = APIRouter()

# 사용자 데이터 저장소
user_data_store = {}
async def get_user(session_id: str):
    if not session_id or session_id not in user_data_store:
        raise HTTPException(status_code=404, detail="Session not found")
    return user_data_store.get(session_id)


# 세션 ID를 생성하는 함수
def create_session():
    return str(uuid4())

# 사용자 세션 생성 + 세션값 반환
@router.get("/api/users/create-session",
            responses={
            200: {
                "content": {
                "application/json": {
                    "example": {
                        "session_id": "user_session_id"}
                }
            }
            }
        })
async def create_user_session(response: Response = None):
    
    session_id = create_session()  # 새로운 세션 ID 생성
    user_data_store[session_id] = User(emotion=None, playlist=None)
        
    # 쿠키에 HttpOnly 속성을 추가하여 JavaScript에서 접근할 수 없게 만듦
    response.set_cookie(key="session_id", value=session_id, httponly=True, path="/")
        
    # 사용자의 세션ID 반환
    return {"session_id": session_id}

# Restart : 사용자 세선 삭제 후 새로운 세션 데이터 생성
@router.get("/api/users/restart-session",
            responses={
            200: {
                "content": {
                "application/json": {
                    "example": {
                        "session_id": "new_user_session_id"}
                }
            }
            }
        })
async def restart_session(session_id: str = Cookie(None), response: Response = None):
    # 세션 ID가 없거나 유효하지 않으면 오류 반환
    await get_user(session_id)
    
    # 기존 세션 데이터 삭제 후 새로운 세션 데이터 생성
    del user_data_store[session_id]
    new_session_id = create_session()  # 새로운 세션 ID 생성
    user_data_store[new_session_id] = User(emotion=None, playlist=None)
    
    # 쿠키에 HttpOnly 속성을 추가하여 JavaScript에서 접근할 수 없게 만듦
    response.set_cookie(key="session_id", value=new_session_id, httponly=True, path="/")
    
    return {"session_id": new_session_id}
      
# 세션으로 사용자 데이터 조회
@router.get("/api/users/", response_model=User)
async def get_user_data(session_id: Optional[str] = Cookie(None)):
    return await get_user(session_id) 
