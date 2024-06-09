from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from core.api.models import LimitHistory
from core.api.serializers import LimitHistorySerializer

class LimitHistoryListCreateView(ListCreateAPIView):
    queryset = LimitHistory.objects.all()
    serializer_class = LimitHistorySerializer
    permission_classes = [IsAuthenticated]

class LimitHistoryRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = LimitHistory.objects.all()
    serializer_class = LimitHistorySerializer
    permission_classes = [IsAuthenticated]

class LimitHistorysByEmissionLimitView(ListAPIView):
    serializer_class = LimitHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        emission_limit_id = self.kwargs['emission_limit_id']
        return LimitHistory.objects.filter(emission_limit_id=emission_limit_id)
