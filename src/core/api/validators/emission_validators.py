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


def validate_unique_default_for_institution(instance):
    from core.api.models import EmissionLimit

    if instance.institution and instance.is_default:
        existing_defaults = EmissionLimit.objects.filter(
            institution=instance.institution, is_default=True
        ).exclude(id=instance.id)
        if existing_defaults.exists():
            raise ValidationError(
                f"Ya existe un límite de emisión predeterminado para la institución {instance.institution}."
            )
