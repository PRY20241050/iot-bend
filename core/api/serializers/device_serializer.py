from rest_framework import serializers

from core.api.models import Device

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }
    
# class DeviceSerializer(serializers.ModelSerializer):
#     # number = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = Device
#         fields = '__all__'
#         extra_kwargs = {
#             'id': {'read_only': True},
#             'created_at': {'read_only': True},
#             'updated_at': {'read_only': True},
#         }
    
#     # def get_number(self, obj):
#     #     return obj.get_number()
