FROM python:3.12-slim

LABEL maintainer="nico"
LABEL description="Pygame Portal Protector with Pygbag"

WORKDIR /app

# System-Dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python Dependencies via requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Game-Dateien kopieren
COPY . /app/

EXPOSE 8000

CMD ["pygbag", "--title", "PortalProtector", "script"]
