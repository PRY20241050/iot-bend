from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from core.api.models import Sensor
from core.api.serializers import SensorSerializer

class SensorListCreateView(ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [IsAuthenticated]

class SensorRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [IsAuthenticated]

class SensorsByDeviceView(ListAPIView):
    serializer_class = SensorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        device_id = self.kwargs['device_id']
        return Sensor.objects.filter(device_id=device_id)
