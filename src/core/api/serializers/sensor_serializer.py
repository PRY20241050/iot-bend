from rest_framework import serializers
from .measurement_serializer import MeasurementSerializer

from core.api.models import Sensor


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = "__all__"

    def validate(self, data):
        device = data.get("device")
        gas_type = data.get("gas_type")

        if Sensor.objects.filter(device=device, gas_type=gas_type).exists():
            raise serializers.ValidationError(
                "Este dispositivo ya está vinculado a este tipo de gas."
            )

        return data


class SensorWithLastMeasurementSerializer(serializers.ModelSerializer):
    last_measurement = serializers.SerializerMethodField()

    class Meta:
        model = Sensor
        fields = "__all__"

    @staticmethod
    def get_last_measurement(self, obj):
        last_measurement = obj.measurement_set.order_by("-date").first()
        if last_measurement:
            return MeasurementSerializer(last_measurement).data
        return None
