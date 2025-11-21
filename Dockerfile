FROM ubuntu:24.04

LABEL maintainer="nico"
LABEL description="Pygame Portal Protector with Pygbag"

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Python 3.12 ist in Ubuntu 24.04 bereits dabei
RUN apt-get update && apt-get install -y \
    python3.12 \
    python3.12-venv \
    python3-pip \
    gcc \
    g++ \
    make \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Python als Standard
RUN ln -s /usr/bin/python3.12 /usr/bin/python

# Pip upgraden
RUN python3.12 -m pip install --upgrade pip

COPY requirements.txt .
RUN python3.12 -m pip install --no-cache-dir -r requirements.txt
RUN python3.12 -m pip install --no-cache-dir black

COPY . /app/

EXPOSE 8000

CMD ["python3.12", "-m", "pygbag", "--title", "PortalProtector", "script"]
