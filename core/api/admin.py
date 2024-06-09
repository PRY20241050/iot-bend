from django.contrib import admin
from .models import Brickyard, Institution, Management, Device, GasType, Sensor

class ManagementInline(admin.TabularInline):
    model = Management
    extra = 1

class SensorInline(admin.TabularInline):
    model = Sensor
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

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    model = Device
    list_display = ['id', 'name', 'status', 'battery_level', 'brickyard']
    inlines = [SensorInline]

@admin.register(GasType)
class GasTypeAdmin(admin.ModelAdmin):
    model = GasType
    list_display = ['name', 'abbreviation']
    
@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    model = Sensor
    list_display = ['device', 'gas_type']

