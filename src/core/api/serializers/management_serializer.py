from rest_framework import serializers

from core.api.models import Management


class ManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Management
        fields = "__all__"
