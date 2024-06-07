from django.db import models

class Measurement(models.Model):
    value = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Valor')
    date = models.DateTimeField(auto_now_add=False, blank=True, null=True, verbose_name='Fecha')
    
    sensor = models.ForeignKey('api.Sensor', on_delete=models.CASCADE, blank=False, null=False, verbose_name='Sensor')
    gas_type = models.ForeignKey('api.Status', on_delete=models.CASCADE, blank=False, null=False, verbose_name='Estado')
    
    def __str__(self):
        return self.value
    
    class Meta:
        db_table = 'medicion'

class Status(models.Model):
    name = models.CharField(max_length=50, blank=False, verbose_name='Nombre')
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'estado_medicion'
