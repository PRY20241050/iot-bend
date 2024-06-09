from rest_framework import serializers

from core.api.models import Brickyard

class BrickyardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brickyard
        fields = '__all__'
