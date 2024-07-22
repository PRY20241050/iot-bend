# validators.py
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_brickyard_and_institution(obj):
    if obj.brickyard and obj.institution:
        raise ValidationError(
            _("No se puede pertenecer a una ladrillera y una institución al mismo tiempo")
        )
