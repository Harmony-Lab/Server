# 빌드 단계
FROM python:3.9-slim AS builder
WORKDIR /test
COPY ./requirements.txt /test/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /test/requirements.txt

# 실행 단계
FROM python:3.9-slim
WORKDIR /test
# 패키지 복사
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
# 실행 파일 복사
COPY --from=builder /usr/local/bin /usr/local/bin
COPY ./src /test/src

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
