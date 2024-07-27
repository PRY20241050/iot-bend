from rest_framework.permissions import IsAuthenticated
from core.api.models import Management, Institution, Brickyard
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from core.utils.response import custom_response
from rest_framework.generics import ListCreateAPIView
from core.api.serializers import ManagementSerializer


class ManagementListCreateView(ListCreateAPIView):
    """
    Handle GET and POST requests for management.
    """

    serializer_class = ManagementSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Add multiple brickyards to an institution.
        <institution_id> is the ID of the institution.
        [brickyard_ids] is a list of brickyard IDs.
        """
        institution = get_object_or_404(Institution, pk=self.kwargs["institution_id"])
        brickyard_ids = request.data.get("brickyard_ids", [])

        if not isinstance(brickyard_ids, list):
            return custom_response(
                "brickyard_ids debe ser una lista de IDs", status.HTTP_400_BAD_REQUEST
            )

        created_count = 0
        for brickyard_id in brickyard_ids:
            try:
                brickyard = Brickyard.objects.get(pk=brickyard_id)
            except Brickyard.DoesNotExist:
                continue

            response = Management.objects.get_or_create(
                institution=institution, brickyard=brickyard
            )
            if response[1]:
                created_count += 1

        return custom_response(
            f"{created_count} ladrilleras añadidas a la institución", status.HTTP_201_CREATED
        )


# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def add_brickyard_to_institution(request, institution_id, brickyard_id):
#     """
#     Add a brickyard to an institution.
#     <institution_id> is the ID of the institution.
#     <brickyard_id> is the ID of the brickyard.
#     """
#
#     institution = get_object_or_404(Institution, pk=institution_id)
#     brickyard = get_object_or_404(Brickyard, pk=brickyard_id)
#
#     try:
#         Management.objects.create(institution=institution, brickyard=brickyard)
#         return custom_response("Ladrillera añadida a la institución", status.HTTP_201_CREATED)
#     except Exception as e:
#         return custom_response(str(e), status.HTTP_400_BAD_REQUEST)
