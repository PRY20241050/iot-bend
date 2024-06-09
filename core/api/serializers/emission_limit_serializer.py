from rest_framework import serializers

from core.api.models import EmissionLimit

class EmissionLimitSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmissionLimit
        fields = '__all__'
