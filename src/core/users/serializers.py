from rest_framework import serializers
from .models import CustomUser as User
from core.api.serializers import BrickyardSerializer, InstitutionSerializer
from .validators import validate_brickyard_and_institution
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    brickyard = BrickyardSerializer(read_only=True)
    institution = InstitutionSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "is_active",
            "role",
            "is_staff",
            "is_superuser",
            "brickyard",
            "institution",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "is_staff": {"read_only": True},
            "is_superuser": {"read_only": True},
        }

    def validate(self, data):
        user = self.Meta.model(**data)
        validate_brickyard_and_institution(user)

        if not user.brickyard and not user.institution:
            data["is_staff"] = True
            data["is_superuser"] = True

        return data

    def create(self, validated_data):
        password = validated_data["password"]
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user

        if not user.brickyard and not user.institution:
            raise AuthenticationFailed(_("No se puede iniciar sesión con este usuario"))

        return data


# Password Reset
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class SetNewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
