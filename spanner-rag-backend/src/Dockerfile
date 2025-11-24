# Use the official Python 3.11 image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
# Upgrade pip and install requirements
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose port 8080 (Vertex AI default)
EXPOSE 8080

# Start the application using uvicorn
# Note: We bind to 0.0.0.0 to ensure external access within the container
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
