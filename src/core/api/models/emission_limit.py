from django.db import models
from core.api.validators import (
    validate_institution_brickyard_management,
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
    gap_time = models.IntegerField(
        default=0,
        verbose_name="Tiempo entre alertas (segundos)",
        help_text="Tiempo en segundos que debe pasar para que se envíe una nueva alertas. Por defecto: 0",
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name="Público",
        help_text="Este límite de emisión puede ser visto por las ladrilleras",
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name="Activo",
    )

    institution = models.ForeignKey(
        "api.Institution",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Institución",
    )
    brickyard = models.ForeignKey(
        "api.Brickyard",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Ladrillera",
    )
    management = models.ForeignKey(
        "api.Management",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Administración",
    )

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última actualización")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "limite_emision"
        verbose_name = "Límite de emisión"
        verbose_name_plural = "Límites de emisión"

    def clean(self):
        if not self.pk:
            super().clean()
            validate_institution_brickyard_management(
                self.institution, self.brickyard, self.management
            )
        else:
            if self.institution or self.brickyard or self.management:
                validate_institution_brickyard_management(
                    self.institution, self.brickyard, self.management
                )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
