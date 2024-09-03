from rest_framework import serializers

from core.api.models import Device
from .sensor_serializer import SensorSerializer


class BaseDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }


class DeviceSerializer(BaseDeviceSerializer):
    class Meta(BaseDeviceSerializer.Meta):
        pass


class DeviceWithSensorsSerializer(BaseDeviceSerializer):
    sensors = SensorSerializer(many=True, read_only=True, source="sensor_set")

    class Meta(BaseDeviceSerializer.Meta):
        pass
