from rest_framework import serializers
from .models import CustomUser as User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'role', 'is_staff', 'is_superuser', 'brickyard', 'institution']
        extra_kwargs = {'password': {'write_only': True}, 'is_staff': {'read_only': True}, 'is_superuser': {'read_only': True}}
        
    def validate(self, data):
        brickyard = data.get('brickyard')
        institution = data.get('institution')
        
        if brickyard and institution:
            raise serializers.ValidationError("El usuario no puede pertener a una ladrillera y una institución al mismo tiempo")
        
        if not brickyard and not institution:
            data['is_staff'] = True
            data['is_superuser'] = True
            
        return data
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
