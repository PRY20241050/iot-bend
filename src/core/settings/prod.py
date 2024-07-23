from .common import *

PRODUCTION = True

PROD_DJANGO_APPS = []

PROD_THIRD_PARTY_APPS = []

PROD_APPS = []

INSTALLED_APPS += PROD_DJANGO_APPS + PROD_THIRD_PARTY_APPS + PROD_APPS

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
