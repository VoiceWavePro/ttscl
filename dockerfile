FROM python:3.10-slim s
# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Upgrade pip and use legacy resolver
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --use-deprecated=legacy-resolver

COPY . .

# Expose port explicitly
EXPOSE 5000

CMD ["python", "app.py"]
