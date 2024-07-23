from rest_framework.response import Response
from rest_framework import status


def create_response(detail: str = None, status_code=status.HTTP_200_OK, **kwargs):
    if detail is None:
        return Response(kwargs, status=status_code)

    response_data = {"detail": detail}
    response_data.update(kwargs)
    return Response(response_data, status=status_code)
