# 실행 단계
FROM python:3.9-slim
WORKDIR /test
COPY ./requirements.txt /test/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /test/requirements.txt
COPY ./src /test/src

RUN python -c "import tensorflow as tf; print(tf.__version__)"
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]