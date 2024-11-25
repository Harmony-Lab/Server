FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /test

# 의존성 설치
COPY ./requirements.txt /test/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /test/requirements.txt \
    && pip install --upgrade typing_extensions

# 애플리케이션 복사
COPY ./src /test/src

# TensorFlow 버전 출력 (디버깅용)
RUN python -c "import tensorflow as tf; print(tf.__version__)"

# FastAPI 서버 실행
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
