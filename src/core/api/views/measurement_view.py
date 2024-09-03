from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    CreateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from core.api.models import Measurement, Device
from core.api.serializers import (
    MeasurementSerializer,
    MeasurementResumenSerializer,
    CreateMeasurementSerializer,
    MeasurementResumenGroupedSerializer,
    MeasurementGroupedByGasSerializer,
)
from core.api.services import MeasurementService
from core.utils.response import custom_response
from core.utils.mixins import OptionalPaginationMixin


class MeasurementCreateView(CreateAPIView):
    """Handle POST requests for measurement data."""

    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    permission_classes = [IsAuthenticated]


class MeasurementAPICreateView(CreateAPIView):
    """Handle POST requests where all measurements data is sent at once."""

    serializer_class = CreateMeasurementSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        device = (
            Device.objects.select_related("brickyard")
            .prefetch_related("sensor_set")
            .get(id=data["deviceId"])
        )
        datetime_obj = parse_datetime(f"{data['date']} {data['time']}")
        brickyard = device.brickyard

        measurements = MeasurementService.save_measurements(data, datetime_obj, device)

        device.status = True
        device.save(update_fields=["status", "updated_at"])

        exceeded_limits = MeasurementService.check_exceeded_limits(measurements, brickyard)
        MeasurementService.schedule_device_deactivation(device)
        if exceeded_limits:
            MeasurementService.handle_alerts_and_notifications(exceeded_limits, brickyard)

        return custom_response("Guardado exitosamente", status.HTTP_201_CREATED)


class MeasurementRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """Handle GET, PUT, PATCH, and DELETE requests for a single measurement."""

    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    permission_classes = [IsAuthenticated]


class MeasurementHistoryView(OptionalPaginationMixin, ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        group_by = self.request.query_params.get("group_by")
        if group_by:
            return MeasurementResumenGroupedSerializer
        return MeasurementResumenSerializer

    def get_queryset(self):
        params = MeasurementService.get_query_params(self.request)
        return MeasurementService.get_measurements(params)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        return self.paginate_if_needed(queryset)


class MeasurementGroupedByGasView(OptionalPaginationMixin, ListAPIView):
    serializer_class = MeasurementGroupedByGasSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        params = MeasurementService.get_query_params(self.request)
        grouped_data = MeasurementService.get_measurements_grouped_by_gas(params)
        return grouped_data

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        return self.paginate_if_needed(queryset)
