from typing import TypeVar, Generic
from rest_framework.response import Response
from core.api.pagination import GenericPagination

T = TypeVar("T", bound="BaseView")


class OptionalPaginationMixin(Generic[T]):
    def paginate_if_needed(self: T, queryset):
        """
        Handle optional pagination based on the 'paginated' query parameter.
        """
        params = self.get_query_params()
        if params.get("paginated"):
            # Activate pagination for this specific request
            self.pagination_class = GenericPagination
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

        # Return non-paginated response
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
