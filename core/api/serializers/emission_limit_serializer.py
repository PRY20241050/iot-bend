from rest_framework import serializers
from core.api.models import EmissionLimit
from core.api.validators import validate_institution_management, validate_unique_default_for_institution

class EmissionLimitSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmissionLimit
        fields = '__all__'
    
    def validate(self, data):
        validate_institution_management(data.get('institution'), data.get('management'))
        validate_unique_default_for_institution(EmissionLimit(**data))
        return data
