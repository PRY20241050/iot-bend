from rest_framework import serializers
from core.api.models import Status, Measurement


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = "__all__"


class MeasurementGroupedPeriodeSerializer(serializers.Serializer):
    date = serializers.DateTimeField()
    device_name = serializers.CharField(source="sensor__device__name")
    gas_abbreviation = serializers.CharField(source="sensor__gas_type__abbreviation")
    value = serializers.DecimalField(max_digits=9, decimal_places=4)


class MeasurementPaginationSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(source="sensor.device.name", read_only=True)
    gas_abbreviation = serializers.CharField(source="sensor.gas_type.abbreviation", read_only=True)

    class Meta:
        model = Measurement
        fields = ["id", "device_name", "gas_abbreviation", "date", "value"]


class CreateMeasurementSerializer(serializers.ModelSerializer):
    deviceId = serializers.IntegerField()
    date = serializers.DateField()
    time = serializers.TimeField()
    pm25 = serializers.DecimalField(max_digits=9, decimal_places=4)
    pm10 = serializers.DecimalField(max_digits=9, decimal_places=4)
    co = serializers.DecimalField(max_digits=9, decimal_places=4)
    no2 = serializers.DecimalField(max_digits=9, decimal_places=4)
    so2 = serializers.DecimalField(max_digits=9, decimal_places=4)
    temperature = serializers.DecimalField(
        max_digits=9, decimal_places=4, required=False, allow_null=True
    )

    class Meta:
        model = Measurement
        fields = [
            "deviceId",
            "date",
            "time",
            "pm25",
            "pm10",
            "co",
            "no2",
            "so2",
            "temperature",
        ]
