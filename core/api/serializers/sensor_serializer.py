from rest_framework import serializers
from .measurement_serializer import MeasurementSerializer

from core.api.models import Sensor

class SensorSerializer(serializers.ModelSerializer):
    measurements = MeasurementSerializer(many=True, read_only=True, source='measurement_set')
    
    class Meta:
        model = Sensor
        fields = '__all__'
        
    def validate(self, data):
        device = data.get('device')
        gas_type = data.get('gas_type')

        if Sensor.objects.filter(device=device, gas_type=gas_type).exists():
            raise serializers.ValidationError("Este dispositivo ya está vinculado a este tipo de gas.")
        
        return data