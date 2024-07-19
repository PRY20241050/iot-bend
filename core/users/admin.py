from django.contrib import admin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'brickyard', 'institution', 'is_staff', 'is_superuser']


admin.site.register(CustomUser, CustomUserAdmin)
