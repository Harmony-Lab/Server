from fastapi import FastAPI
# emotions 라우터 import
from src.routers.emotions import router as emotions_router

app = FastAPI()
app.include_router(emotions_router)  # 라우터 포함

@app.get("/")
async def root():
    return {"message": "Hello World"}
