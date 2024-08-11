from django.db import models


class Alert(models.Model):
    name = models.CharField(max_length=150, blank=True, verbose_name="Nombre")
    short_description = models.TextField(
        max_length=300, blank=True, verbose_name="Descripción corta"
    )
    description = models.TextField(max_length=500, blank=True, verbose_name="Descripción")
    is_read = models.BooleanField(default=False, verbose_name="Leído")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última actualización")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, verbose_name="Usuario")

    def __str__(self):
        return self.name

    def is_owner(self, user):
        return self.user == user

    class Meta:
        db_table = "alerta"
        verbose_name = "Alerta"
        verbose_name_plural = "Alertas"
        ordering = ["-created_at"]
