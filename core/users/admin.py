from django.contrib import admin
from .models import CustomUser
from core.admin.admin import admin_site

class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'brickyard', 'institution', 'is_staff', 'is_superuser']

admin_site.register(CustomUser, CustomUserAdmin)
