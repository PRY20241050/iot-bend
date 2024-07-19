from rest_framework import serializers

from core.api.models import LimitHistory


class LimitHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LimitHistory
        fields = "__all__"
