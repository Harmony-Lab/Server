from fastapi import FastAPI

# 라우터 import
from src.routers.emotions import router as emotions_router
from src.routers.users import router as users_router
from src.routers.playlists import router as playlists_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="MoodTune",
    description="MoodTune의 API 문서입니다.",
)

app.include_router(emotions_router)  # 라우터 포함
app.include_router(users_router)  # 라우터 포함
app.include_router(playlists_router)  # 라우터 포함

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처 허용
    allow_credentials=True, # 쿠키와 인증 정보를 포함할 수 있도록 설정
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

@app.get("/")
async def root():
    return {"message": "Hello World"}