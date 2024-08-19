from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)
from core.api.models import EmissionLimit
from core.api.serializers import EmissionLimitWithLimitHistorySerializer
from core.utils import split_string
from core.utils.consts import IS_TRUE
from core.utils.mixins import OptionalPaginationMixin


class EmissionLimitListCreateView(OptionalPaginationMixin, ListCreateAPIView):
    """
    Handle GET and POST requests for emission limits.
    """

    serializer_class = EmissionLimitWithLimitHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        params = self.get_query_params()

        filters = self.build_filters(params)

        return EmissionLimit.objects.filter(filters).distinct().order_by("id")

    @staticmethod
    def build_filters(params):
        query_filter = Q()

        if params["is_default"]:
            query_filter &= Q(is_default=params["is_default"])

        if params["is_public"]:
            query_filter &= Q(is_public=params["is_public"])

        if params["brickyard_id"] is not None:
            query_filter &= Q(brickyard=params["brickyard_id"])

        if params["institution_id"] is not None:
            query_filter &= Q(institution=params["institution_id"])

        if params["id"]:
            query_filter &= Q(pk=params["id"])

        return query_filter

    def get_query_params(self):
        """
        Query Parameters:
        - is_default        (bool): Return only default emission limits.
        - is_public         (bool): Return only public emission limits.
        - brickyard_id      (int) : Return only emission limits that are associated with a specific brickyard.
        - institution_id    (int) : Return only emission limits that are associated with a specific institution.
        - id                (int) : Return emission limit by ID.
        - paginated         (bool): Return paginated results if true.
        """

        query_params = self.request.query_params
        return {
            "is_default": query_params.get("is_default") in IS_TRUE,
            "is_public": query_params.get("is_public") in IS_TRUE,
            "brickyard_id": query_params.get("brickyard_id"),
            "institution_id": query_params.get("institution_id"),
            "id": query_params.get("id"),
            "paginated": query_params.get("paginated") in IS_TRUE,
        }

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        return self.paginate_if_needed(queryset)


class EmissionLimitByManagementView(ListAPIView):
    """
    Handle GET requests for emission limits by management ID.
    """

    serializer_class = EmissionLimitWithLimitHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        management_id = self.kwargs["management_id"]
        return EmissionLimit.objects.filter(management_id=management_id)


class EmissionLimitByInstitutionView(OptionalPaginationMixin, ListAPIView):
    """
    Handle GET requests for emission limits by institution ID.
    """

    serializer_class = EmissionLimitWithLimitHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        institution_id = self.kwargs["institution_id"]

        params = self.get_query_params()
        filters = self.build_filters(institution_id, params)

        return EmissionLimit.objects.filter(filters).distinct().order_by("id")

    @staticmethod
    def build_filters(institution_id, params):
        query_filter = Q(institution_id=institution_id)

        if params["brickyard_ids"]:
            brickyard_filter = Q(brickyard_id__in=params["brickyard_ids"])
            query_filter |= brickyard_filter

        if params["add_brickyard"]:
            brickyard_filter = Q(brickyard__isnull=False)
            query_filter |= brickyard_filter

        if params["add_management"]:
            management_filter = Q(management__institution_id=institution_id)
            query_filter |= management_filter

        return query_filter

    def get_query_params(self):
        """
        Query Parameters:
        - add_brickyard     (bool): Add brickyard limits to the results.
        - brickyard_ids     (list): Add emission limits that are associated with specific brickyards.
        - add_management    (bool): Add management limits to the results.
        - paginated         (bool): Return paginated results if true.
        """

        query_params = self.request.query_params
        return {
            "add_brickyard": query_params.get("add_brickyard") in IS_TRUE,
            "brickyard_ids": split_string(query_params.get("brickyard_ids")),
            "add_management": query_params.get("add_management") in IS_TRUE,
            "paginated": query_params.get("paginated") in IS_TRUE,
        }

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        return self.paginate_if_needed(queryset)


class EmissionLimitByBrickyardView(OptionalPaginationMixin, ListAPIView):
    """
    Handle GET requests for emission limits by institution ID.
    """

    serializer_class = EmissionLimitWithLimitHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        brickyard_id = self.kwargs["brickyard_id"]

        params = self.get_query_params()
        filters = self.build_filters(brickyard_id, params)

        return EmissionLimit.objects.filter(filters).distinct().order_by("id")

    @staticmethod
    def build_filters(brickyard_id, params):
        query_filter = Q(brickyard_id=brickyard_id)

        if params["add_institution"]:
            institution_filter = Q(institution__isnull=False)
            if params["is_public"]:
                institution_filter &= Q(is_public=params["is_public"])
            query_filter |= institution_filter

        if params["add_management"]:
            management_filter = Q(management__brickyard_id=brickyard_id)
            if params["is_public"]:
                management_filter &= Q(is_public=params["is_public"])
            query_filter |= management_filter

        return query_filter

    def get_query_params(self):
        """
        Query Parameters:
        - add_institution   (bool): Add institution limits to the results.
        - add_management    (bool): Add management limits to the results.
        - is_public         (bool): Institution limits are public.
        - paginated         (bool): Return paginated results if true.
        """

        query_params = self.request.query_params
        return {
            "is_public": query_params.get("is_public") in IS_TRUE,
            "add_institution": query_params.get("add_institution") in IS_TRUE,
            "add_management": query_params.get("add_management") in IS_TRUE,
            "paginated": query_params.get("paginated") in IS_TRUE,
        }

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        return self.paginate_if_needed(queryset)


class EmissionLimitRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    Handle GET, PUT, PATCH and DELETE requests for a single emission limit.
    """

    queryset = EmissionLimit.objects.all()
    serializer_class = EmissionLimitWithLimitHistorySerializer
    permission_classes = [IsAuthenticated]
