# Use the latest stable Python image as the base
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Update package lists and install necessary dependencies
RUN apt-get update && apt-get install -y \
    python3-apt \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip and setuptools
RUN pip install --no-cache-dir --upgrade pip setuptools

# Copy the requirements file first for better caching during dependency installation
COPY requirements.txt .

# Install dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Install additional dependencies
RUN pip install --no-cache-dir psycopg2-binary rq

# Copy the source code into the container
COPY src/ ./src/

# Set environment variables
ENV DATABASE_URL=postgresql://user:password@db:5432/leetcode_compiler
ENV PYTHONUNBUFFERED=1

# Expose the Flask app port
EXPOSE 7000

# Define the command to run the API server
CMD ["python", "src/api/main.py"]
