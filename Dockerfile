# ==========================================================================
# Okumpi website — single production container
# Django 6.0.7 + gunicorn + WhiteNoise + SQLite (on a volume at /data)
# ==========================================================================
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_DEBUG=0 \
    DJANGO_BEHIND_PROXY=1 \
    DJANGO_DB_DIR=/data

WORKDIR /app

# Dependencies first (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Project code
COPY . .

# Ensure the entrypoint is executable (Windows checkouts lose the +x bit)
RUN chmod +x /app/docker-entrypoint.sh

# Pre-build the static bundle into the image
RUN python manage.py collectstatic --noinput

# Non-root user; /data holds the SQLite database (mounted as a volume)
RUN useradd --create-home okumpi \
    && mkdir -p /data \
    && chown -R okumpi:okumpi /app /data
USER okumpi

EXPOSE 8080

ENTRYPOINT ["/app/docker-entrypoint.sh"]
