from django.db import models

CO_ID = 1
NO2_ID = 2
SO2_ID = 3
PM25_ID = 4
PM10_ID = 5
TEMPERATURE_ID = 6


class GasType(models.Model):
    name = models.CharField(max_length=100, blank=False, verbose_name="Nombre")
    abbreviation = models.CharField(max_length=10, blank=False, verbose_name="Abreviatura")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última actualización")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tipo_gas"
        verbose_name = "Tipo de gas"
        verbose_name_plural = "Tipos de gas"
