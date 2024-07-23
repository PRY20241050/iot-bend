from django.urls import path, include
from . import views

urlpatterns = [
    path("", include("core.users.urls")),
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
    path(
        "institution/<int:institution_id>/brickyard/<int:brickyard_id>/",
        views.add_brickyard_to_institution,
        name="add-brickyard-to-institution",
    ),
    path(
        "institution/<int:institution_id>/add_brickyards/",
        views.add_multiple_brickyards_to_institution,
        name="add-brickyards-to-institution",
    ),
    # using (params: brickyard_id)
    path("devices/", views.DeviceListCreateView.as_view(), name="device-list-create"),
    # using
    path(
        "devices/<int:pk>/",
        views.DeviceRetrieveUpdateDestroyView.as_view(),
        name="device-detail",
    ),
    # using
    path(
        "devices/<int:device_id>/sensors/last_measurements/",
        views.SensorLastMeasurementView.as_view(),
        name="sensor_last_measurements",
    ),
    path("gases/", views.GasTypeListCreateView.as_view(), name="gas-list-create"),
    path(
        "gases/<int:pk>/",
        views.GasTypeRetrieveUpdateDestroyView.as_view(),
        name="gas-detail",
    ),
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
    path("status/", views.StatusListCreateView.as_view(), name="status-list-create"),
    path(
        "status/<int:pk>/",
        views.StatusRetrieveUpdateDestroyView.as_view(),
        name="status-detail",
    ),
    path("measurements/", views.MeasurementListView.as_view(), name="measurement-list"),
    path(
        "measurements/create/",
        views.MeasurementCreateView.as_view(),
        name="measurement-create",
    ),
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
    # using (params: brickyard_ids)
    path(
        "measurements/paginated/",
        views.MeasurementPaginatedListView.as_view(),
        name="measurement-paginated-list",
    ),
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
        views.LimitHistorysByEmissionLimitView.as_view(),
        name="limit-history-by-emission-limit",
    ),
]
