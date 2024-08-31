from django.core.exceptions import ValidationError


def validate_institution_brickyard_management(institution, brickyard, management):
    if not institution and not management and not brickyard:
        raise ValidationError(
            "Debe seleccionar una institución, una ladrillera o una administración."
        )
    if (
        institution
        and management
        or institution
        and brickyard
        or management
        and brickyard
        or institution
        and management
        and brickyard
    ):
        raise ValidationError(
            "Solo puede seleccionar una institución, una ladrillera o una administración."
        )
