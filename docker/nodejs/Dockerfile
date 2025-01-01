# nodejs/Dockerfile
FROM node:16-slim
WORKDIR /leetcode_compiler
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/* && \
    adduser --disabled-password --gecos '' executor
USER executor
CMD ["node"]