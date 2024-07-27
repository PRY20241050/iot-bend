from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)
from rest_framework.permissions import IsAuthenticated
from core.api.models import LimitHistory
from core.api.serializers import LimitHistorySerializer


class LimitHistoryListCreateView(ListCreateAPIView):
    """
    Handle GET and POST requests for limit history data.
    """

    queryset = LimitHistory.objects.all()
    serializer_class = LimitHistorySerializer
    permission_classes = [IsAuthenticated]


class LimitHistoryRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    Handle GET, PUT, PATCH, and DELETE requests for a single limit history.
    """

    queryset = LimitHistory.objects.all()
    serializer_class = LimitHistorySerializer
    permission_classes = [IsAuthenticated]


class LimitHistoryByEmissionLimitView(ListAPIView):
    """
    Handle GET requests for limit history by emission limit ID.
    """

    serializer_class = LimitHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        emission_limit_id = self.kwargs["emission_limit_id"]
        return LimitHistory.objects.filter(emission_limit_id=emission_limit_id)
