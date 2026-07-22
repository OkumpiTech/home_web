#!/bin/sh
# Okumpi container start-up: migrate → seed (first run only) → serve.
set -e

echo "==> Applying database migrations"
python manage.py migrate --noinput

echo "==> Seeding content (skipped automatically if data already exists)"
python manage.py seed_okumpi || true

echo "==> Starting gunicorn on :8080"
exec gunicorn okumpi.wsgi:application \
    --bind 0.0.0.0:8080 \
    --workers "${GUNICORN_WORKERS:-3}" \
    --timeout 60 \
    --access-logfile - \
    --error-logfile -
