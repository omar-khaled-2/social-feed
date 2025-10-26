# Use an official Python base image
FROM python:3.14-slim

# Set working directory inside the container
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev 


# Copy dependency file first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

# Command to run the app
CMD ["python", "run.py"]
