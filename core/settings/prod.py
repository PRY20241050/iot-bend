from .common import *

PROD_DJANGO_APPS = []

PROD_THIRD_PARTY_APPS = [
    "corsheaders",
]

PROD_APPS = []

INSTALLED_APPS += PROD_DJANGO_APPS + PROD_THIRD_PARTY_APPS + PROD_APPS

MIDDLEWARE.insert(1, "corsheaders.middleware.CorsMiddleware")

# CORS settings
# https://pypi.org/project/django-cors-headers/

ALLOWED_HOSTS_CORS = [
    f"http://{host}" if not host.startswith(("http://", "https://")) else host
    for host in ALLOWED_HOSTS
    if host not in ("*", "localhost", "127.0.0.1", "[::1]")
]

ALLOWED_HOSTS_CORS.extend(
    [
        "http://localhost",
        "https://localhost",
        "http://127.0.0.1",
        "https://127.0.0.1",
        "http://[::1]",
        "https://[::1]",
        # ".vercel.app",
    ]
)

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = ALLOWED_HOSTS_CORS

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
# TODO: replace media and static files with S3

STATICFILES_DIRS = [
    BASE_DIR / "static",
    BASE_DIR / "media",
]

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_ROOT = BASE_DIR / "mediafiles"
