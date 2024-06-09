from core.api.models import Device
from core.api.serializers import DeviceSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView

class DeviceListCreateView(ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]

class DeviceRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]

class DeviceByBrickyardView(ListAPIView):
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        brickyard_id = self.kwargs['brickyard_id']
        return Device.objects.filter(brickyard_id=brickyard_id)
