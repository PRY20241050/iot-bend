from core.api.models import EmissionLimit
from core.api.serializers import EmissionLimitSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView

class EmissionLimitListCreateView(ListCreateAPIView):
    queryset = EmissionLimit.objects.all()
    serializer_class = EmissionLimitSerializer
    permission_classes = [IsAuthenticated]

class EmissionLimitRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = EmissionLimit.objects.all()
    serializer_class = EmissionLimitSerializer
    permission_classes = [IsAuthenticated]

class EmissionLimitByManagementView(ListAPIView):
    serializer_class = EmissionLimitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        management_id = self.kwargs['management_id']
        return EmissionLimit.objects.filter(management_id=management_id)
