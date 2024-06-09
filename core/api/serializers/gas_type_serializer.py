from rest_framework import serializers

from core.api.models import GasType

class GasTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GasType
        fields = '__all__'
