from django.contrib.auth.models import AbstractUser
from django.db import models
from .validators import validate_brickyard_and_institution


class CustomUser(AbstractUser):
    email = models.EmailField("Correo electrónico", blank=False, unique=True)
    role = models.CharField("Rol", max_length=50, blank=True, default="")

    brickyard = models.ForeignKey("api.Brickyard", on_delete=models.CASCADE, blank=True, null=True)
    institution = models.ForeignKey(
        "api.Institution", on_delete=models.CASCADE, blank=True, null=True
    )

    def clean(self):
        validate_brickyard_and_institution(self)
        super().clean()

    class Meta:
        db_table = "auth_user"
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
