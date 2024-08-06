from django.urls import path, include
from . import views

# Users URLs
users_patterns = [
    path("", include("core.users.urls")),
]

# Brickyards URLs
brickyards_patterns = [
    path(
        "brickyards/",
        views.BrickyardListCreateView.as_view(),
        name="brickyard-list-create",
    ),
    path(
        "brickyards/<int:pk>/",
        views.BrickyardRetrieveUpdateDestroyView.as_view(),
        name="brickyard-detail",
    ),
]

# Institutions URLs
institutions_patterns = [
    path(
        "institution/",
        views.InstitutionListCreateView.as_view(),
        name="institution-list-create",
    ),
    path(
        "institution/<int:pk>/",
        views.InstitutionRetrieveUpdateDestroyView.as_view(),
        name="institution-detail",
    ),
]

# Management URLs
management_patterns = [
    path(
        "institution/<int:institution_id>/add_brickyards/",
        views.ManagementListCreateView.as_view(),
        name="add-brickyards-to-institution",
    ),
]

# Devices URLs
devices_patterns = [
    # using (params: brickyard_id)
    path("devices/", views.DeviceListCreateView.as_view(), name="device-list-create"),
    # using
    path(
        "devices/<int:pk>/",
        views.DeviceRetrieveUpdateDestroyView.as_view(),
        name="device-detail",
    ),
]

# Gases URLs
gases_patterns = [
    path("gases/", views.GasTypeListCreateView.as_view(), name="gas-list-create"),
    path(
        "gases/<int:pk>/",
        views.GasTypeRetrieveUpdateDestroyView.as_view(),
        name="gas-detail",
    ),
]

# Sensors URLs
sensors_patterns = [
    path("sensors/", views.SensorListCreateView.as_view(), name="sensor-list-create"),
    path(
        "sensors/<int:pk>/",
        views.SensorRetrieveUpdateDestroyView.as_view(),
        name="sensor-detail",
    ),
    path(
        "device/<int:device_id>/sensors/",
        views.SensorsByDeviceView.as_view(),
        name="sensors-by-device",
    ),
]

# Measurements URLs
measurements_patterns = [
    path("measurements/", views.MeasurementCreateView.as_view(), name="measurement-create"),
    path(
        "measurements/<int:pk>/",
        views.MeasurementRetrieveUpdateDestroyView.as_view(),
        name="measurement-detail",
    ),
    path(
        "sensor/<int:sensor_id>/measurements/",
        views.MeasurementBySensorView.as_view(),
        name="measurements-by-sensor",
    ),
    # using
    path(
        "devices/<int:device_id>/sensors/last_measurements/",
        views.SensorLastMeasurementView.as_view(),
        name="sensor_last_measurements",
    ),
    path(
        "measurements/create/",
        views.MeasurementAPICreateView.as_view(),
        name="measurement-api-create",
    ),
    # using (params: brickyard_ids)
    path(
        "measurements/paginated/",
        views.MeasurementPaginatedListView.as_view(),
        name="measurement-paginated-list",
    ),
]

# Status URLs
status_patterns = [
    path("status/", views.StatusListView.as_view(), name="status-list"),
    path(
        "status/<int:pk>/",
        views.StatusRetrieveUpdateDestroyView.as_view(),
        name="status-detail",
    ),
]

# Emission Limits URLs
emission_limits_patterns = [
    path(
        "emission_limits/",
        views.EmissionLimitListCreateView.as_view(),
        name="emission-limit-list-create",
    ),
    path(
        "emission_limits/<int:pk>/",
        views.EmissionLimitRetrieveUpdateDestroyView.as_view(),
        name="emission-limit-detail",
    ),
    path(
        "management/<int:management_id>/emission_limits/",
        views.EmissionLimitByManagementView.as_view(),
        name="emission-limits-by-management",
    ),
]

# Limit History URLs
limit_history_patterns = [
    path(
        "limit_history/",
        views.LimitHistoryListCreateView.as_view(),
        name="limit-history-list-create",
    ),
    path(
        "limit_history/<int:pk>/",
        views.LimitHistoryRetrieveUpdateDestroyView.as_view(),
        name="limit-history-detail",
    ),
    path(
        "emission_limit/<int:emission_limit_id>/limit_history/",
        views.LimitHistoryByEmissionLimitView.as_view(),
        name="limit-history-by-emission-limit",
    ),
]

urlpatterns = (
    users_patterns
    + brickyards_patterns
    + institutions_patterns
    + management_patterns
    + devices_patterns
    + gases_patterns
    + sensors_patterns
    + measurements_patterns
    + status_patterns
    + emission_limits_patterns
    + limit_history_patterns
)
