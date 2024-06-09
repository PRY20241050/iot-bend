from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from . import models

admin.site.site_header = _('Sistema de monitoreo IoT')
admin.site.site_title = _('Sistema de monitoreo IoT')
admin.site.index_title = _('Bienvenido al sistema de monitoreo IoT')

class ManagementInline(admin.TabularInline):
    model = models.Management
    extra = 1

class SensorInline(admin.TabularInline):
    model = models.Sensor
    extra = 1

class MeasurementInline(admin.TabularInline):
    model = models.Measurement
    extra = 1

@admin.register(models.Brickyard)
class BrickyardAdmin(admin.ModelAdmin):
    model = models.Brickyard
    list_display = ['name', 'address', 'ruc', 'phone', 'contact']

@admin.register(models.Institution)
class InstitutionAdmin(admin.ModelAdmin):
    model = models.Institution
    list_display = ['name', 'address', 'phone', 'contact']
    inlines = [ManagementInline]

@admin.register(models.Management)
class ManagementAdmin(admin.ModelAdmin):
    model = models.Management
    list_display = ['institution', 'brickyard']

@admin.register(models.Device)
class DeviceAdmin(admin.ModelAdmin):
    model = models.Device
    list_display = ['id', 'name', 'status', 'battery_level', 'brickyard']
    inlines = [SensorInline]

@admin.register(models.GasType)
class GasTypeAdmin(admin.ModelAdmin):
    model = models.GasType
    list_display = ['name', 'abbreviation']
    
@admin.register(models.Sensor)
class SensorAdmin(admin.ModelAdmin):
    model = models.Sensor
    list_display = ['id', 'device', 'gas_type']
    inlines = [MeasurementInline]
    
@admin.register(models.Status)
class StatusAdmin(admin.ModelAdmin):
    model = models.Status
    list_display = ['name']

@admin.register(models.Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    model = models.Measurement
    list_display = ['id', 'sensor', 'status', 'value', 'date']
