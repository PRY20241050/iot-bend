from rest_framework import serializers

from core.api.models import LimitHistory


class BaseLimitHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LimitHistory
        exclude = ["created_at", "updated_at"]


class LimitHistorySerializer(BaseLimitHistorySerializer):
    class Meta(BaseLimitHistorySerializer.Meta):
        pass
