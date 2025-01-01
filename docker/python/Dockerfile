# For python/Dockerfile:
    FROM python:3.9-slim
    WORKDIR /leetcode_compiler
    RUN adduser --disabled-password --gecos '' executor && \
        apt-get update && \
        apt-get install -y --no-install-recommends \
        python3-pip \
        && rm -rf /var/lib/apt/lists/*
    USER executor
    CMD ["python3"]
    
