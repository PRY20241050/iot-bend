from django.contrib import admin
from . import models
from rangefilter.filters import DateTimeRangeFilterBuilder


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
    list_display = ["id", "name", "address", "ruc", "phone", "contact"]


class InstitutionAdmin(admin.ModelAdmin):
    model = models.Institution
    list_display = ["id", "name", "address", "phone", "contact"]
    inlines = [ManagementInline]


class ManagementAdmin(admin.ModelAdmin):
    model = models.Management
    list_display = ["institution", "brickyard"]


class DeviceAdmin(admin.ModelAdmin):
    model = models.Device
    list_display = ["id", "name", "status", "brickyard"]
    inlines = [SensorInline]


class GasTypeAdmin(admin.ModelAdmin):
    model = models.GasType
    list_display = ["id", "name", "abbreviation"]


class SensorAdmin(admin.ModelAdmin):
    model = models.Sensor
    list_display = ["id", "device", "gas_type"]
    inlines = [MeasurementInline]


class StatusAdmin(admin.ModelAdmin):
    model = models.Status
    list_display = ["name"]


class MeasurementAdmin(admin.ModelAdmin):
    model = models.Measurement
    list_display = ["id", "sensor", "status", "value", "date"]
    list_filter = (
        ("date", DateTimeRangeFilterBuilder()),
        "sensor",
        "sensor__device__name",
        "sensor__device__brickyard__name",
    )


class EmissionLimitAdmin(admin.ModelAdmin):
    model = models.EmissionLimit
    list_display = [
        "id",
        "name",
        "email_alert",
        "app_alert",
        "institution",
        "brickyard",
        "management",
        "is_active",
        "is_public",
    ]
    inlines = [LimitHistoryInline]


class AlertAdmin(admin.ModelAdmin):
    model = models.Alert
    list_display = ["id", "name", "is_read", "created_at", "user"]
    list_filter = ["user"]


admin.site.register(models.Brickyard, BrickyardAdmin)
admin.site.register(models.Institution, InstitutionAdmin)
admin.site.register(models.Management, ManagementAdmin)
admin.site.register(models.Device, DeviceAdmin)
admin.site.register(models.GasType, GasTypeAdmin)
admin.site.register(models.Sensor, SensorAdmin)
admin.site.register(models.Status, StatusAdmin)
admin.site.register(models.Measurement, MeasurementAdmin)
admin.site.register(models.EmissionLimit, EmissionLimitAdmin)
admin.site.register(models.Alert, AlertAdmin)
