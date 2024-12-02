from fastapi import FastAPI

# 라우터 import
from src.routers.emotions import router as emotions_router
from src.routers.users import router as users_router
from src.routers.playlists import router as playlists_router

# Middleware import
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

import tensorflow as tf

# FastAPI 애플리케이션 초기화
app = FastAPI(
    title="MoodTune",
    description="MoodTune의 API 문서입니다.",
    version="1.0.0",
)

# 라우터 등록
app.include_router(emotions_router, prefix="/emotions", tags=["Emotions"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(playlists_router, prefix="/playlists", tags=["Playlists"])

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처 허용
    allow_credentials=True,  # 쿠키와 인증 정보를 포함할 수 있도록 설정
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

tf_version = tf.__version__
print(f"TensorFlow version: {tf_version}")

# 기본 엔드포인트
@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to MoodTune API!"}