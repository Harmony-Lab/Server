from fastapi import APIRouter, HTTPException, Response, Cookie
from src.models.user import User
from typing import Optional
from uuid import uuid4
import jwt
import datetime
from datetime import timezone

router = APIRouter()

# 비밀 키와 알고리즘 설정
SECRET_KEY = "your_secret_key"  # 비밀 키는 안전하게 관리해야 합니다.
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 토큰 만료 시간 설정

# 사용자 데이터 저장소
user_data_store = {}

async def get_user(session_id: str):
    if not session_id or session_id not in user_data_store:
        raise HTTPException(status_code=404, detail="Session not found")
    return user_data_store.get(session_id)


# JWT 토큰 생성 함수
def create_jwt_token(user_id: str):
    expiration = datetime.datetime.now(timezone.utc) + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = jwt.encode({"sub": user_id, "exp": expiration}, SECRET_KEY, algorithm=ALGORITHM)
    return token

# 사용자 세션 생성하고 JWT 토큰 반환
@router.get("/create-session",
            responses={
            200: {
                "content": {
                "application/json": {
                    "example": {
                        "token": "user_access_token"}
                }
            }
            }
        })
async def create_user_session(response: Response = None):
    user_id = str(uuid4())  # 사용자 ID 생성
    user_data_store[user_id] = User(emotion=None, playlist=None)
        
    access_token = create_jwt_token(user_id)  # JWT 토큰 생성
    
    # JWT 토큰을 쿠키에 저장
    response.set_cookie(key="token", value=access_token, httponly=True)
        
    return {"token": access_token}

# Restart : 사용자 세션 삭제 후 새로운 세션 데이터 생성하여 JWT 토큰 반환
@router.get("/restart-session",
            responses={
            200: {
                "content": {
                "application/json": {
                    "example": {
                        "token": "new_user_access_token"}
                }
            }
            }
        })
async def restart_session(response: Response, token: str = Cookie(None)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        
        # 기존 사용자 데이터 삭제
        if user_id in user_data_store:
            del user_data_store[user_id]
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    new_user_id = str(uuid4())  # 새로운 사용자 ID 생성
    user_data_store[new_user_id] = User(emotion=None, playlist=None)

    new_access_token = create_jwt_token(new_user_id)  # 새로운 JWT 토큰 생성
    
    # 새로운 JWT 토큰을 쿠키에 저장
    response.set_cookie(key="token", value=new_access_token, httponly=True)
    
    return {"token": new_access_token}
      
# JWT 토큰으로 사용자 데이터 조회
@router.get("/", response_model=User)
async def get_user_data(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        return await get_user(user_id)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")