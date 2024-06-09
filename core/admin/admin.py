from django.templatetags.static import static
from django.contrib.admin.sites import AdminSite
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin
from django.contrib.sites.admin import SiteAdmin

class MyAdminSite(AdminSite):
    site_header = _("Sistema de monitoreo IoT")
    site_title = _("Sistema de monitoreo IoT")
    index_title = _("Bienvenido al sistema de monitoreo IoT")

    def get_urls(self):
        urls = super().get_urls()
        return urls

    def each_context(self, request):
        context = super().each_context(request)
        context['admin_custom_css'] = static('admin/admin_custom.css')
        return context

admin_site = MyAdminSite(name='myadmin')

admin_site.register(Site, SiteAdmin)
admin_site.register(Group, GroupAdmin)
