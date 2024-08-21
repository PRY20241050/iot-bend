from rest_framework import serializers
from core.api.models import Status, Measurement


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = "__all__"


class CreateMeasurementSerializer(serializers.Serializer):
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
        fields = "__all__"


class MeasurementResumenGroupedSerializer(serializers.Serializer):
    device_name = serializers.CharField(source="sensor__device__name")
    gas_abbreviation = serializers.CharField(source="sensor__gas_type__abbreviation")
    gas_type = serializers.IntegerField(source="sensor__gas_type__id", read_only=True)
    date = serializers.DateTimeField()
    value = serializers.DecimalField(max_digits=9, decimal_places=4)


class MeasurementResumenSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(source="sensor.device.name", read_only=True)
    gas_abbreviation = serializers.CharField(source="sensor.gas_type.abbreviation", read_only=True)
    gas_type = serializers.IntegerField(source="sensor.gas_type.id", read_only=True)

    class Meta:
        model = Measurement
        fields = ["id", "device_name", "gas_abbreviation", "gas_type", "date", "value"]


class MeasurementGroupedByGasSerializer(serializers.Serializer):
    gas_type = serializers.IntegerField(read_only=True)
    gas_abbreviation = serializers.CharField(read_only=True)
    measurements = serializers.ListField(child=serializers.DictField())
    avg = serializers.DecimalField(max_digits=9, decimal_places=4)
    max = serializers.DecimalField(max_digits=9, decimal_places=4)
    min = serializers.DecimalField(max_digits=9, decimal_places=4)


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"
