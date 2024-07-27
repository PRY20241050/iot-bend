from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from core.api.models import GasType
from core.api.serializers import GasTypeSerializer


class GasTypeListCreateView(ListCreateAPIView):
    """
    Handle GET and POST requests for gas type data.
    """

    queryset = GasType.objects.all()
    serializer_class = GasTypeSerializer


class GasTypeRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    Handle GET, PUT, PATCH, and DELETE requests for a single gas type.
    """

    queryset = GasType.objects.all()
    serializer_class = GasTypeSerializer
