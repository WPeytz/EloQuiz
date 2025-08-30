# Use an official Python runtime as a parent image
FROM --platform=linux/amd64 python:3.11-slim

# Set the working directory in the container
WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/serviceAccountKey.json

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Copy serviceAccountKey.json
COPY serviceAccountKey.json ./serviceAccountKey.json

# Expose the default Cloud Run port
EXPOSE 8080

# Run the application
CMD ["gunicorn", "-b", "0.0.0.0:8080", "main:app", "--workers", "1", "--threads", "8", "--timeout", "0", "--access-logfile", "-", "--error-logfile", "-", "--log-level", "info"]
