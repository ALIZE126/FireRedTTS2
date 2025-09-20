FROM python:3.12-slim

WORKDIR /app
COPY . /app

COPY requirements.txt .

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        libgomp1 \
        libsndfile1 \
        ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

# 用国内源加速
RUN pip install --no-cache-dir -r requirements.txt \
    --extra-index-url https://pypi.tuna.tsinghua.edu.cn/simple/ \
    --extra-index-url https://mirrors.aliyun.com/pypi/simple/


EXPOSE 8000
CMD ["python", "-m", "uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]