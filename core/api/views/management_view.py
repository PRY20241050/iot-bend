from rest_framework.permissions import IsAuthenticated
from core.api.models import Management, Institution, Brickyard
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_brickyard_to_institution(request, institution_id, brickyard_id):
    try:
        institution = Institution.objects.get(pk=institution_id)
        brickyard = Brickyard.objects.get(pk=brickyard_id)
        Management.objects.create(institution=institution, brickyard=brickyard)
        return Response({"status": "Ladrillera añadida a la institución"}, status=status.HTTP_201_CREATED)
    except Institution.DoesNotExist:
        return Response({"error": "Institución no encontrada"}, status=status.HTTP_404_NOT_FOUND)
    except Brickyard.DoesNotExist:
        return Response({"error": "Ladrillera no encontrada"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_multiple_brickyards_to_institution(request, institution_id):
    try:
        institution = Institution.objects.get(pk=institution_id)
    except Institution.DoesNotExist:
        return Response({"error": "Institución no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    brickyard_ids = request.data.get('brickyard_ids', [])
        
    if not isinstance(brickyard_ids, list):
        return Response({"error": "brickyard_ids debe ser una lista de IDs"}, status=status.HTTP_400_BAD_REQUEST)

    created_count = 0
    for brickyard_id in brickyard_ids:
        try:
            brickyard = Brickyard.objects.get(pk=brickyard_id)
            Management.objects.get_or_create(institution=institution, brickyard=brickyard)
            created_count += 1
        except Brickyard.DoesNotExist:
            continue

    return Response({"status": f"{created_count} ladrilleras añadidas a la institución"}, status=status.HTTP_201_CREATED)
