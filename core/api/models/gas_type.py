from django.db import models

class GasType(models.Model):
    name = models.CharField(max_length=100, blank=True, verbose_name='Nombre')

    last_update = models.DateTimeField(auto_now=True, verbose_name='Última actualización')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'tipo_gas'
