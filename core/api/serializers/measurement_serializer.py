from rest_framework import serializers

from core.api.models import Status, Measurement

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = '__all__'

class CreateMeasurementSerializer(serializers.ModelSerializer):
    deviceId = serializers.IntegerField()
    date = serializers.DateField()
    time = serializers.TimeField()
    pm25 = serializers.DecimalField(max_digits=12, decimal_places=8)
    pm10 = serializers.DecimalField(max_digits=12, decimal_places=8)
    co = serializers.DecimalField(max_digits=12, decimal_places=8)
    no2 = serializers.DecimalField(max_digits=12, decimal_places=8)
    so2 = serializers.DecimalField(max_digits=12, decimal_places=8)
    
    class Meta:
        model = Measurement
        fields = ['deviceId', 'date', 'time', 'pm25', 'pm10', 'co', 'no2', 'so2']
