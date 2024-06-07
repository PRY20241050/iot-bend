from rest_framework import serializers

from core.api.models import Device

class DeviceSerializer(serializers.ModelSerializer):
    # number = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Device
        fields = [
            'name',
            'description',
            'status',
            'battery_level',
            # 'status_text',
            # 'number'
        ] 
    
    # def get_number(self, obj):
    #     return obj.get_number()
