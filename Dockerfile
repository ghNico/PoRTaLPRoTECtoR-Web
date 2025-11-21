FROM python:3.12-slim

LABEL maintainer="nico"
LABEL description="Pygame Portal Protector with Pygbag"

WORKDIR /app

# Erweiterte System-Dependencies für Pygame + Pygbag
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    ffmpeg \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    && rm -rf /var/lib/apt/lists/*

# Python Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Optional: Black für Code-Optimierung
RUN pip install --no-cache-dir black

# Game-Dateien kopieren
COPY . /app/

EXPOSE 8000

CMD ["pygbag", "--title", "PortalProtector", "script"]
