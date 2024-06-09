from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from core.api.models import GasType
from core.api.serializers import GasTypeSerializer

class GasTypeListCreateView(ListCreateAPIView):
    queryset = GasType.objects.all()
    serializer_class = GasTypeSerializer

class GasTypeRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = GasType.objects.all()
    serializer_class = GasTypeSerializer

