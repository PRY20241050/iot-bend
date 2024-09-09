from django.db import models


class Device(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    description = models.TextField(max_length=500, blank=True, verbose_name="Descripción")
    status = models.BooleanField(default=False, verbose_name="Está activado")
    battery_level = models.DecimalField(
        max_digits=5, decimal_places=2, default=0, verbose_name="Nivel de batería"
    )

    brickyard = models.ForeignKey(
        "api.Brickyard",
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name="Ladrillera",
    )

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última actualización")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "dispositivo"
        verbose_name = "Dispositivo"
        verbose_name_plural = "Dispositivos"

    # @property
    # def status_text(self):
    #     return 'On' if self.status else 'Off'

    # def get_number(self):
    #     return 100
