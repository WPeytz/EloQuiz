# Use an official Python runtime as a parent image
FROM python:3.13-alpine

# Set the working directory in the container
WORKDIR /app

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
CMD ["gunicorn", "-b", ":8080", "main:app"]
