from core.api.models import Device
from core.api.serializers import DeviceSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class DeviceListCreateView(ListCreateAPIView):
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        brickyard_id = self.request.query_params.get("brickyard_id", None)
        if brickyard_id is not None:
            return Device.objects.filter(brickyard_id=brickyard_id)
        return Device.objects.all()


class DeviceRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]
