# Dockerfile for main API server
FROM python:3.12

WORKDIR /app
RUN apt-get update && apt-get install -y python3-apt && \
pip install --upgrade pip setuptools

# Install dependencies
COPY requirements.txt . 

RUN pip install -r requirements.txt
RUN pip install psycopg2-binary
RUN pip install rq

# Copy source code
COPY src/ ./src/
ENV DATABASE_URL=postgresql://user:password@db:5432/leetcode_compiler
# Set environment variables
ENV PYTHONUNBUFFERED=1
EXPOSE 7000

CMD ["python", "src/api/main.py"]
