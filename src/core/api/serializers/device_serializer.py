from rest_framework import serializers

from core.api.models import Device
from .sensor_serializer import SensorSerializer


class DeviceSerializer(serializers.ModelSerializer):
    sensors = SensorSerializer(many=True, read_only=True, source="sensor_set")

    class Meta:
        model = Device
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
            "created_at": {"read_only": True},
            "last_update": {"read_only": True},
        }
