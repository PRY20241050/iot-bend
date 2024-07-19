from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from core.api.models import Brickyard
from core.api.serializers import BrickyardSerializer


class BrickyardListCreateView(ListCreateAPIView):
    queryset = Brickyard.objects.all()
    serializer_class = BrickyardSerializer
    permission_classes = [IsAuthenticated]


class BrickyardRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Brickyard.objects.all()
    serializer_class = BrickyardSerializer
    permission_classes = [IsAuthenticated]
