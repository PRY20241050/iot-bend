from django.db import models

class Sensor(models.Model):
    device = models.ForeignKey('api.Device', on_delete=models.CASCADE, blank=False, null=False)
    gas_type = models.ForeignKey('api.GasType', on_delete=models.CASCADE, blank=False, null=False)

    last_update = models.DateTimeField(auto_now=True, verbose_name='Última actualización')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'sensor'
