import os
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .tokens import account_activation_token
from .serializers import (
    UserSerializer,
    ChangePasswordSerializer,
    PasswordResetSerializer,
    SetNewPasswordSerializer,
)
from .models import CustomUser as User


class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class UserDetailView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.data.get("old_password")):
                return Response(
                    {"detail": "Contraseña incorrecta."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if serializer.data.get("old_password") == serializer.data.get("new_password"):
                return Response(
                    {"detail": "La nueva contraseña no puede ser igual a la anterior."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response(
                {"detail": "La contraseña se cambió con éxito."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data["email"]
            user = User.objects.filter(email=email).first()
            if user:
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = account_activation_token.make_token(user)
                reset_link = f"{os.getenv('FRONTEND_RECOVER_URL', '')}/?uid={uid}&token={token}"
                mail_subject = "Restablecer contraseña"
                message = render_to_string(
                    "password_reset_email.html",
                    {
                        "user": user,
                        "reset_link": reset_link,
                    },
                )
                send_mail(mail_subject, message, "from@example.com", [user.email])
                return Response({"detail": "El email fue enviado"}, status=status.HTTP_200_OK)
            return Response(
                {"email": "No se encontró un usuario asociado a este correo"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uid, token, *args, **kwargs):
        serializer = SetNewPasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                uid = force_str(urlsafe_base64_decode(uid))
                user = User.objects.get(pk=uid)
                if account_activation_token.check_token(user, token):
                    user.set_password(serializer.data["new_password"])
                    user.save()
                    return Response(
                        {"detail": "La contraseña fue restablecida"},
                        status=status.HTTP_200_OK,
                    )
                return Response({"token": "Token inválido"}, status=status.HTTP_400_BAD_REQUEST)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                return Response({"uid": "Usuario inválido"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
