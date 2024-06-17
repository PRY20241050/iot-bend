from core.api.models import EmissionLimit
from core.api.serializers import EmissionLimitSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView

class EmissionLimitListCreateView(ListCreateAPIView):
    serializer_class = EmissionLimitSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = EmissionLimit.objects.all()
        is_default = self.request.query_params.get('is_default', None)
        is_institution = self.request.query_params.get('is_institution', None)
        if is_default is not None:
            queryset = queryset.filter(is_default=is_default)
        
        if is_institution is not None:
            queryset = queryset.filter(institution__isnull=False)
        return queryset

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
