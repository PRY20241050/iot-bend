from .common import *

PRODUCTION = False

DEV_DJANGO_APPS = []

DEV_THIRD_PARTY_APPS = [
    "django_browser_reload",
    "debug_toolbar",
    "corsheaders",
]

DEV_APPS = []

INSTALLED_APPS += DEV_DJANGO_APPS + DEV_THIRD_PARTY_APPS + DEV_APPS

MIDDLEWARE.insert(1, "debug_toolbar.middleware.DebugToolbarMiddleware")
MIDDLEWARE.insert(2, "corsheaders.middleware.CorsMiddleware")
MIDDLEWARE.append("django_browser_reload.middleware.BrowserReloadMiddleware")

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
    ]
)

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = ALLOWED_HOSTS_CORS

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATICFILES_DIRS = [
    BASE_DIR / "static",
    BASE_DIR / "media",
]

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

STATIC_ROOT = BASE_DIR.parent / "staticfiles"
MEDIA_ROOT = BASE_DIR / "mediafiles"
