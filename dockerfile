# Use Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy templates and app files
COPY templates/ templates/
COPY . .

# Expose new port
EXPOSE 8080

# Run app on port 8080
CMD ["python", "app.py"]
