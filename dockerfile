FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Upgrade pip and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt --use-deprecated=legacy-resolver

# Copy app code
COPY . .

# Expose Flask port
EXPOSE 5000

# Start server
CMD ["python", "app.py"]
