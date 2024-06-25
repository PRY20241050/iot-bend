from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from core.admin.admin import admin_site
from . import models

class ManagementInline(admin.TabularInline):
    model = models.Management
    extra = 1

class SensorInline(admin.TabularInline):
    model = models.Sensor
    extra = 1

class MeasurementInline(admin.TabularInline):
    model = models.Measurement
    extra = 1

class LimitHistoryInline(admin.TabularInline):
    model = models.LimitHistory
    extra = 1

class BrickyardAdmin(admin.ModelAdmin):
    model = models.Brickyard
    list_display = ['name', 'address', 'ruc', 'phone', 'contact']

class InstitutionAdmin(admin.ModelAdmin):
    model = models.Institution
    list_display = ['name', 'address', 'phone', 'contact']
    inlines = [ManagementInline]

class ManagementAdmin(admin.ModelAdmin):
    model = models.Management
    list_display = ['institution', 'brickyard']

class DeviceAdmin(admin.ModelAdmin):
    model = models.Device
    list_display = ['id', 'name', 'status', 'battery_level', 'brickyard']
    inlines = [SensorInline]

class GasTypeAdmin(admin.ModelAdmin):
    model = models.GasType
    list_display = ['id', 'name', 'abbreviation']

class SensorAdmin(admin.ModelAdmin):
    model = models.Sensor
    list_display = ['id', 'device', 'gas_type']
    inlines = [MeasurementInline]

class StatusAdmin(admin.ModelAdmin):
    model = models.Status
    list_display = ['name']

class MeasurementAdmin(admin.ModelAdmin):
    model = models.Measurement
    list_display = ['id', 'sensor', 'status', 'value', 'date']

class EmissionLimitAdmin(admin.ModelAdmin):
    model = models.EmissionLimit
    list_display = ['id', 'name', 'email_alert', 'app_alert', 'management', 'institution', 'is_default']
    inlines = [LimitHistoryInline]
    
class AlertAdmin(admin.ModelAdmin):
    model = models.Alert
    list_display = ['id', 'name', 'is_read', 'date']

admin_site.register(models.Brickyard, BrickyardAdmin)
admin_site.register(models.Institution, InstitutionAdmin)
admin_site.register(models.Management, ManagementAdmin)
admin_site.register(models.Device, DeviceAdmin)
admin_site.register(models.GasType, GasTypeAdmin)
admin_site.register(models.Sensor, SensorAdmin)
admin_site.register(models.Status, StatusAdmin)
admin_site.register(models.Measurement, MeasurementAdmin)
admin_site.register(models.EmissionLimit, EmissionLimitAdmin)
admin_site.register(models.Alert, AlertAdmin)
