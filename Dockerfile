# backend/Dockerfile
FROM python:3.12.3-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    proj-bin \
    libproj-dev \
    build-essential \
    gcc \
    python3-dev \
 && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && gunicorn photomap.wsgi:application --bind 0.0.0.0:8000"]

