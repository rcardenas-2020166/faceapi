FROM python:3.11-slim

WORKDIR /app

# Dependencias de sistema requeridas por mediapipe/sounddevice
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libportaudio2 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8001}"]
