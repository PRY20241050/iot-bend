from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from core.api.models import Device
from core.api.serializers import DeviceWithSensorsSerializer, DeviceSerializer
from django.utils import timezone
from core.utils.consts import IS_TRUE


class DeviceListCreateView(ListCreateAPIView):
    """Handle GET and POST requests for device data."""

    permission_classes = [IsAuthenticated]
    queryset = Device.objects.all()

    def get_serializer_class(self):
        params = self.get_query_params()
        if params["with_sensors"]:
            return DeviceWithSensorsSerializer
        return DeviceSerializer

    def get_queryset(self):
        params = self.get_query_params()

        if params["brickyard_id"]:
            # Update device status
            devices = self.queryset.filter(brickyard_id=params["brickyard_id"])
            update_devices = devices.prefetch_related("sensor_set__measurement_set")
            for device in update_devices:
                now = timezone.now()
                last_measurement = (
                    device.sensor_set.order_by("id")
                    .first()
                    .measurement_set.order_by("-date")
                    .first()
                )
                if last_measurement:
                    if (now - last_measurement.date).total_seconds() > 90:
                        device.status = False
                        device.save()

            return devices
        return self.get_queryset().all()

    def get_query_params(self):
        """
        Query Parameters:
        - brickyard_id (int): Filter devices by brickyard ID.
        - with_sensors (bool): Include sensors data in the response.
        """

        query_params = self.request.query_params

        return {
            "brickyard_id": query_params.get("brickyard_id"),
            "with_sensors": query_params.get("with_sensors") in IS_TRUE,
        }


class DeviceRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """Handle GET, PUT, PATCH, and DELETE requests for a single device."""

    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]
