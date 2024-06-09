from core.api.models import Status, Measurement
from core.api.serializers import StatusSerializer, MeasurementSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView

class StatusListCreateView(ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

class StatusRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    
class MeasurementListCreateView(ListCreateAPIView):
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
