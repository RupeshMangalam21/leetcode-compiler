# Dockerfile for main API server
FROM python:3.9

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source code
COPY src/ /app/src/

# Set environment variables
ENV PYTHONUNBUFFERED=1

CMD ["python", "src/api/main.py"]
