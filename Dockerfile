# Base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /test

# Install system dependencies for TensorFlow and OpenGL
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY ./requirements.txt /test/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /test/requirements.txt

# Copy application source code
COPY ./src /test/src

# Verify TensorFlow installation and CUDA compatibility
RUN python -c "import tensorflow as tf; print('TensorFlow version:', tf.__version__)" && \
    python -c "from tensorflow.python.client import device_lib; print(device_lib.list_local_devices())"

# Expose FastAPI application port
EXPOSE 8000

# Start FastAPI server
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
