from rest_framework import serializers
from core.api.models import EmissionLimit
from core.api.validators import (
    validate_institution_brickyard_management,
)
from .limit_history_serializer import LimitHistorySerializer


class BaseEmissionLimitSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmissionLimit
        exclude = ["created_at", "updated_at"]

    def validate(self, data):
        validate_institution_brickyard_management(
            data.get("institution"), data.get("brickyard"), data.get("management")
        )
        return data


class EmissionLimitWithLimitHistorySerializer(BaseEmissionLimitSerializer):
    limit_history = LimitHistorySerializer(many=True, read_only=True, source="limithistory_set")

    class Meta(BaseEmissionLimitSerializer.Meta):
        pass
