from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from core.api.models import Device
from core.api.serializers import DeviceSerializer


class DeviceListCreateView(ListCreateAPIView):
    """
    Handle GET and POST requests for device data.
    """

    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]
    queryset = Device.objects.all()

    def get_queryset(self):
        params = self.get_query_params()

        if params["brickyard_id"] is not None:
            return self.queryset.filter(brickyard_id=params["brickyard_id"])
        return self.queryset.all()

    def get_query_params(self):
        """
        Query Parameters:
        - brickyard_id (int): Filter devices by brickyard ID.
        """

        query_params = self.request.query_params

        return {"brickyard_id": query_params.get("brickyard_id")}


class DeviceRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    Handle GET, PUT, PATCH, and DELETE requests for a single device.
    """

    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]
