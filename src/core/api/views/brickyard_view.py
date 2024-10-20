from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from core.api.models import Brickyard
from core.api.serializers import BrickyardSerializer


class BrickyardListCreateView(ListCreateAPIView):
    """
    Handle GET and POST requests for brickyard data.
    """

    queryset = Brickyard.objects.filter(visible=True)
    serializer_class = BrickyardSerializer
    permission_classes = [IsAuthenticated]


class BrickyardRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    Handle GET, PUT, PATCH, and DELETE requests for a single brickyard.
    """

    queryset = Brickyard.objects.all()
    serializer_class = BrickyardSerializer
    permission_classes = [IsAuthenticated]
