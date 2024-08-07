from .common import *

PRODUCTION = False

DEV_DJANGO_APPS = []

DEV_THIRD_PARTY_APPS = [
    "django_browser_reload",
    "debug_toolbar",
]

DEV_APPS = []

INSTALLED_APPS += DEV_DJANGO_APPS + DEV_THIRD_PARTY_APPS + DEV_APPS

MIDDLEWARE.insert(1, "debug_toolbar.middleware.DebugToolbarMiddleware")
MIDDLEWARE.append("django_browser_reload.middleware.BrowserReloadMiddleware")

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
