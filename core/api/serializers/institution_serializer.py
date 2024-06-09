from rest_framework import serializers

from core.api.models import Institution

class InstitutionSerializer(serializers.ModelSerializer):
    brickyards = serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Institution
        fields = '__all__'
