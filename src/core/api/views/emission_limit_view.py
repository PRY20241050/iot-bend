from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)
from rest_framework.response import Response
from core.api.models import EmissionLimit
from core.api.pagination import GenericPagination
from core.api.serializers import EmissionLimitSerializer
from core.utils.consts import IS_TRUE


class EmissionLimitListCreateView(ListCreateAPIView):
    """
    Handle GET and POST requests for emission limits.
    """

    serializer_class = EmissionLimitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        params = self.get_query_params()

        if not params["brickyard_id"]:
            return EmissionLimit.objects.none()

        shared_filter, id_filter, aggregate_filter = self.build_filters(params)
        queryset = EmissionLimit.objects.filter(shared_filter & id_filter)

        if aggregate_filter:
            queryset |= EmissionLimit.objects.filter(shared_filter & aggregate_filter)

        return queryset.distinct().order_by("management_id", "institution_id")

    def get_query_params(self):
        """
        Query Parameters:
        - is_default        (bool): Return only default emission limits.
        - is_public         (bool): Return only public emission limits.
        - show_institution  (bool): Return only emission limits that are associated with an institution.
        - show_management   (bool): Return only emission limits that are associated with a management.
        - brickyard_id      (int) : Return only emission limits that are associated with a specific brickyard.
        - institution_id    (int) : Return only emission limits that are associated with a specific institution.
        - paginated         (bool): Return paginated results if true.
        """

        query_params = self.request.query_params
        return {
            "is_default": query_params.get("is_default") in IS_TRUE,
            "is_public": query_params.get("is_public") in IS_TRUE,
            "show_institution": query_params.get("show_institution") in IS_TRUE,
            "show_management": query_params.get("show_management") in IS_TRUE,
            "brickyard_id": query_params.get("brickyard_id"),
            "institution_id": query_params.get("institution_id"),
            "paginated": query_params.get("paginated") in IS_TRUE,
        }

    @staticmethod
    def build_filters(params):
        shared_filter = Q()
        id_filter = Q()
        aggregate_filter = Q()

        if params["is_default"]:
            shared_filter &= Q(is_default=params["is_default"])

        if params["is_public"]:
            shared_filter &= Q(is_public=params["is_public"])

        if params["brickyard_id"] is not None:
            id_filter &= Q(management__brickyard=params["brickyard_id"])

        if params["institution_id"] is not None:
            id_filter &= Q(institution=params["institution_id"])

        if params["show_institution"]:
            if id_filter == Q():
                shared_filter &= Q(institution__isnull=False)
            else:
                aggregate_filter &= Q(institution__isnull=False)

        if params["show_management"]:
            if id_filter == Q():
                shared_filter &= Q(management__isnull=False)
            else:
                aggregate_filter &= Q(management__isnull=False)

        return shared_filter, id_filter, aggregate_filter

    def list(self, request, *args, **kwargs):
        params = self.get_query_params()
        queryset = self.filter_queryset(self.get_queryset())

        if params["paginated"]:
            # Activamos la paginación para esta solicitud específica
            self.pagination_class = GenericPagination
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

        # Devolvemos sin paginar si no se especifica la paginación
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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
