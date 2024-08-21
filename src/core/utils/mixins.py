from typing import TypeVar, Generic, Callable, Optional
from rest_framework.response import Response
from core.api.pagination import GenericPagination
from core.utils.consts import IS_TRUE

T = TypeVar("T", bound="BaseView")


class OptionalPaginationMixin(Generic[T]):
    def paginate_if_needed(self: T, queryset):
        """
        Handle optional pagination based on the 'paginated' query parameter.
        """
        if self.request.query_params.get("paginated") in IS_TRUE:
            # Activate pagination for this specific request
            self.pagination_class = GenericPagination
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

        # Return non-paginated response
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
