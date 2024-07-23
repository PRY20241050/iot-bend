from django.core.exceptions import ValidationError


def validate_institution_management(institution, management):
    if not institution and not management:
        raise ValidationError("Debe seleccionar una institución o una administración.")
    if institution and management:
        raise ValidationError(
            "No puede seleccionar una institución y una administración al mismo tiempo."
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
