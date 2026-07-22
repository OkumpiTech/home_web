"""
Django settings for the Okumpi website (okumpi_v2).

Django 5.x / 6.x compatible. SQLite database.

All production knobs are environment variables (see .env.example):
    DJANGO_SECRET_KEY           real secret key (required in production)
    DJANGO_DEBUG                "1" (default, dev) or "0" (production)
    DJANGO_ALLOWED_HOSTS        comma-separated, e.g. "okumpi.com,www.okumpi.com"
    DJANGO_CSRF_TRUSTED_ORIGINS comma-separated, e.g. "https://okumpi.com"
    DJANGO_DB_DIR               directory holding db.sqlite3 (default: project root)
    DJANGO_BEHIND_PROXY         "1" when behind Caddy/Nginx TLS proxy (default "0")

With no env vars set, behaviour is identical to development defaults,
so `python manage.py runserver` keeps working exactly as before.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def env_list(name, default=''):
    return [v.strip() for v in os.environ.get(name, default).split(',') if v.strip()]


# SECURITY WARNING: set DJANGO_SECRET_KEY in production.
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-okumpi-v2-dev-key-change-me-in-production')

DEBUG = os.environ.get('DJANGO_DEBUG', '1') == '1'

ALLOWED_HOSTS = env_list('DJANGO_ALLOWED_HOSTS', '*')
# Always allow loopback so the Docker healthcheck and local curl work.
if '*' not in ALLOWED_HOSTS:
    for _h in ('127.0.0.1', 'localhost'):
        if _h not in ALLOWED_HOSTS:
            ALLOWED_HOSTS.append(_h)

CSRF_TRUSTED_ORIGINS = env_list('DJANGO_CSRF_TRUSTED_ORIGINS')

# Behind Caddy (which terminates HTTPS) trust the forwarded proto header.
if os.environ.get('DJANGO_BEHIND_PROXY', '0') == '1':
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    USE_X_FORWARDED_HOST = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'okumpi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.site_globals',
            ],
        },
    },
]

WSGI_APPLICATION = 'okumpi.wsgi.application'

# SQLite — in Docker, DJANGO_DB_DIR points at a persistent volume (/data).
DB_DIR = Path(os.environ.get('DJANGO_DB_DIR', BASE_DIR))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DB_DIR / 'db.sqlite3',
        'OPTIONS': {
            'timeout': 20,
            'init_command': 'PRAGMA journal_mode=WAL; PRAGMA synchronous=NORMAL;',
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Kampala'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# WhiteNoise serves compressed static files straight from gunicorn —
# no separate web server needed inside the container.
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
    },
}

MEDIA_URL = '/media/'
MEDIA_ROOT = Path(os.environ.get('DJANGO_MEDIA_ROOT', BASE_DIR / 'media'))

# Sensible production hardening when DEBUG is off
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SITE_NAME = 'Okumpi'
SITE_TAGLINE = 'Your shortest route to ICT that works'
