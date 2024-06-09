from django.contrib import admin
from .models import Brickyard, Institution, Management

class ManagementInline(admin.TabularInline):
    model = Management
    extra = 1

@admin.register(Brickyard)
class BrickyardAdmin(admin.ModelAdmin):
    model = Brickyard
    list_display = ['name', 'address', 'ruc', 'phone', 'contact']

@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    model = Institution
    list_display = ['name', 'address', 'phone', 'contact']
    inlines = [ManagementInline]

@admin.register(Management)
class ManagementAdmin(admin.ModelAdmin):
    model = Management
    list_display = ['institution', 'brickyard']
