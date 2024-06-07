from django.db import models

class EmissionLimit(models.Model):
    name = models.CharField(max_length=100, blank=True, verbose_name='Nombre')
    description = models.TextField(max_length=250, blank=True, verbose_name='Descripción')
    email_alert = models.BooleanField(default=False, verbose_name='Alerta de correo electrónico')
    app_alert = models.BooleanField(default=False, verbose_name='Alerta de aplicación')

    management = models.ForeignKey('api.Management', on_delete=models.CASCADE, blank=False, null=False, verbose_name='Administración')

    last_update = models.DateTimeField(auto_now=True, verbose_name='Última actualización')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'limite_emision'
