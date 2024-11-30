FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Copy the entire project into the container
COPY . .

# Set the PYTHONPATH to the /app/src directory
ENV PYTHONPATH=/app/src

# Install required dependencies (if any)
RUN pip install -r requirements.txt

# Run the script
CMD ["python3", "src/api/script.py"]
