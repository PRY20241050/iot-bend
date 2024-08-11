from rest_framework import serializers
from core.api.models import EmissionLimit
from core.api.validators import (
    validate_institution_brickyard_management,
    validate_unique_default_for_institution,
)
from .limit_history_serializer import LimitHistorySerializer


class EmissionLimitSerializer(serializers.ModelSerializer):
    limit_history = LimitHistorySerializer(many=True, read_only=True, source="limithistory_set")

    class Meta:
        model = EmissionLimit
        fields = "__all__"

    def validate(self, data):
        validate_institution_brickyard_management(
            data.get("institution"), data.get("brickyard"), data.get("management")
        )
        validate_unique_default_for_institution(EmissionLimit(**data))
        return data
