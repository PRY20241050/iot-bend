from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)
from core.api.models import EmissionLimit
from core.api.serializers import EmissionLimitSerializer
from core.utils.consts import IS_TRUE
from core.utils.response import custom_response
from core.utils.mixins import OptionalPaginationMixin


class EmissionLimitListCreateView(OptionalPaginationMixin, ListCreateAPIView):
    """
    Handle GET and POST requests for emission limits.
    """

    serializer_class = EmissionLimitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        params = self.get_query_params()

        if not params["brickyard_id"]:
            return custom_response("Se debe incluir el brickyard_id", status=400)

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
            id_filter &= Q(brickyard=params["brickyard_id"])

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
        queryset = self.filter_queryset(self.get_queryset())
        return self.paginate_if_needed(queryset)


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


class EmissionLimitByBrickyardView(OptionalPaginationMixin, ListAPIView):
    """
    Handle GET requests for emission limits by institution ID.
    """

    serializer_class = EmissionLimitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        brickyard_id = self.kwargs["brickyard_id"]

        if not brickyard_id:
            return custom_response("Se debe incluir el brickyard_id", status=400)

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
    serializer_class = EmissionLimitSerializer
    permission_classes = [IsAuthenticated]
