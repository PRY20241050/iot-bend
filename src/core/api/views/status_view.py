from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)
from core.api.models import Status
from core.api.serializers import StatusSerializer


class StatusListView(ListAPIView):
    """
    Handle GET requests for status data.
    """

    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class StatusRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    Handle GET, PUT, PATCH, and DELETE requests for a single status.
    """

    queryset = Status.objects.all()
    serializer_class = StatusSerializer
