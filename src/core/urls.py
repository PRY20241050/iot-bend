from django.contrib import admin
from django.urls import path, include
from django.conf import settings

"""
Import the site module to register the site.
This is necessary to make the site config available in the admin interface.
"""
import core.site

# fmt: off
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("core.api.urls"))
]

if not settings.PRODUCTION:
    from django.conf.urls.static import static

    dev_patterns = [
        path("__debug__/", include("debug_toolbar.urls")),
        path("__reload__/", include("django_browser_reload.urls"), name="browser_reload"),
    ]
    urlpatterns = dev_patterns + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
