from django.db import models


class Brickyard(models.Model):
    name = models.CharField(max_length=150, blank=True, verbose_name="Nombre")
    address = models.CharField(max_length=200, blank=True, verbose_name="Dirección")
    ruc = models.CharField(max_length=11, blank=True, verbose_name="RUC")
    phone = models.IntegerField(blank=True, null=True, verbose_name="Teléfono")
    contact = models.CharField(max_length=100, blank=True, verbose_name="Contacto")

    last_update = models.DateTimeField(auto_now=True, verbose_name="Última actualización")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "ladrillera"
        verbose_name = "Ladrillera"
        verbose_name_plural = "Ladrilleras"
