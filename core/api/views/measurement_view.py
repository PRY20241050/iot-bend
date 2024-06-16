from rest_framework import status
from rest_framework.response import Response
from django.utils.dateparse import parse_datetime

from core.api.models import Status, Measurement, Sensor
from core.api.serializers import StatusSerializer, MeasurementSerializer, CreateMeasurementSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView

class StatusListCreateView(ListAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

class StatusRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    
class MeasurementListView(ListCreateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    permission_classes = [IsAuthenticated]

class MeasurementRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    permission_classes = [IsAuthenticated]

class MeasurementBySensorView(ListAPIView):
    serializer_class = MeasurementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        sensor_id = self.kwargs['sensor_id']
        return Measurement.objects.filter(sensor_id=sensor_id)

class MeasurementCreateView(CreateAPIView):
    serializer_class = CreateMeasurementSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        device_id = data['deviceId']
        datetime_str = f"{data['date']} {data['time']}"
        datetime_obj = parse_datetime(datetime_str)

        gas_types = {
            "pm25": 4,
            "pm10": 5,
            "co": 1,
            "no2": 2,
            "so2": 3,
        }

        for gas, gas_id in gas_types.items():
            try:
                sensor = Sensor.objects.get(device_id=device_id, gas_type_id=gas_id)
                Measurement.objects.create(
                    value=data[gas],
                    date=datetime_obj,
                    sensor=sensor
                )
            except Sensor.DoesNotExist:
                return Response({"error": f"No se encontró el sensor para el gas: {gas}"}, status=status.HTTP_400_BAD_REQUEST)

        if 'temperature' in data:
            try:
                temperature_sensor = Sensor.objects.get(device_id=device_id, gas_type_id=6)
                Measurement.objects.create(
                    value=data['temperature'],
                    date=datetime_obj,
                    sensor=temperature_sensor
                )
            except Sensor.DoesNotExist:
                return Response({"error": "No se encontró el sensor para la temperatura"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Guardado exitosamente"}, status=status.HTTP_201_CREATED)
