from django.db import models


class Alert(models.Model):
    name = models.CharField(max_length=150, blank=True, verbose_name="Nombre")
    description = models.TextField(max_length=500, blank=True, verbose_name="Descripción")
    is_read = models.BooleanField(default=False, verbose_name="Leído")
    date = models.DateTimeField(auto_now=True, verbose_name="Fecha")

    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, verbose_name="Usuario")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "alerta"
        verbose_name = "Alerta"
        verbose_name_plural = "Alertas"
        ordering = ["-date"]
