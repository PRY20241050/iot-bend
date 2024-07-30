from rest_framework.response import Response
from rest_framework import status
from django.utils.translation import gettext_lazy as _


def custom_response(
    message: str = None, status_code=status.HTTP_200_OK, key: str = "detail", **kwargs
):
    if message is None:
        return Response(kwargs, status=status_code)

    if status_code not in [status.HTTP_200_OK, status.HTTP_201_CREATED]:
        key = "error"

    response_data = {key: _(message)}
    response_data.update(kwargs)
    return Response(response_data, status=status_code)
