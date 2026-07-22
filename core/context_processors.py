from django.conf import settings


def site_globals(request):
    """Globals available in every template."""
    return {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_TAGLINE': settings.SITE_TAGLINE,
    }
