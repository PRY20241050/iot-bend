from django.db import models
from core.api.validators import (
    validate_institution_management,
    validate_unique_default_for_institution,
)


class EmissionLimit(models.Model):
    name = models.CharField(max_length=100, blank=True, verbose_name="Nombre")
    description = models.TextField(max_length=250, blank=True, verbose_name="Descripción")
    email_alert = models.BooleanField(
        default=False,
        verbose_name="Alerta por correo electrónico",
        help_text="Se enviará una notificación por correo electrónico",
    )
    app_alert = models.BooleanField(
        default=False,
        verbose_name="Alerta por aplicación",
        help_text="Se enviará una notificación a la aplicación",
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name="Público",
        help_text="Este límite de emisión es público",
    )
    is_default = models.BooleanField(
        default=False,
        verbose_name="Predeterminado",
        help_text="Este límite de emisión es el predeterminado",
    )

    institution = models.ForeignKey(
        "api.Institution",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Institución",
    )
    management = models.ForeignKey(
        "api.Management",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Administración",
    )

    last_update = models.DateTimeField(auto_now=True, verbose_name="Última actualización")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "limite_emision"
        verbose_name = "Límite de emisión"
        verbose_name_plural = "Límites de emisión"

    def clean(self):
        super().clean()
        validate_institution_management(self.institution, self.management)
        validate_unique_default_for_institution(self)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
