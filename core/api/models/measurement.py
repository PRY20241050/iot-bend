from django.db import models

class Measurement(models.Model):
    value = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name='Valor', help_text='Medido en mg x m3')
    date = models.DateTimeField(auto_now_add=False, blank=True, null=True, verbose_name='Fecha')
    
    sensor = models.ForeignKey('api.Sensor', on_delete=models.CASCADE, blank=False, null=False, verbose_name='Sensor')
    status = models.ForeignKey('api.Status', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Estado de la lectura')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    
    def __str__(self):
        return self.value.__str__()
    
    class Meta:
        db_table = 'medicion'
        verbose_name = 'Medición'
        verbose_name_plural = 'Mediciones'

class Status(models.Model):
    name = models.CharField(max_length=50, blank=False, verbose_name='Nombre')
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'estado_medicion'
        verbose_name = 'Estado de la medición'
        verbose_name_plural = 'Estados de la medición'
