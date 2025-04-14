# Use Python as the base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY templates/ templates/


# Copy the application code
COPY . .

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]

