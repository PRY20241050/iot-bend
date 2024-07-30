from core.api.models import EmissionLimit
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)
from core.api.serializers import EmissionLimitSerializer


class EmissionLimitListCreateView(ListCreateAPIView):
    """
    Handle GET and POST requests for emission limits.
    """

    serializer_class = EmissionLimitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Query Parameters:
        - is_default        (bool): Return only default emission limits.
        - is_institution    (bool): Return only emission limits that are associated with an institution.
        - is_management     (bool): Return only emission limits that are associated with a management.
        """
        queryset = EmissionLimit.objects.all()
        query_params = self.request.query_params

        is_default = query_params.get("is_default")
        is_institution = query_params.get("is_institution")
        is_management = query_params.get("is_management")

        if is_default is not None:
            queryset = queryset.filter(is_default=is_default)

        if is_institution is not None:
            queryset = queryset.filter(institution__isnull=False)

        if is_management is not None:
            queryset = queryset.filter(management__isnull=False)

        return queryset


class EmissionLimitByManagementView(ListAPIView):
    """
    Handle GET requests for emission limits by management ID.
    """

    serializer_class = EmissionLimitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        management_id = self.kwargs["management_id"]
        return EmissionLimit.objects.filter(management_id=management_id)


class EmissionLimitByInstitutionView(ListAPIView):
    """
    Handle GET requests for emission limits by institution ID.
    """

    serializer_class = EmissionLimitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        institution_id = self.kwargs["institution_id"]
        return EmissionLimit.objects.filter(institution_id=institution_id)


class EmissionLimitRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    Handle GET, PUT, PATCH and DELETE requests for a single emission limit.
    """

    queryset = EmissionLimit.objects.all()
    serializer_class = EmissionLimitSerializer
    permission_classes = [IsAuthenticated]
