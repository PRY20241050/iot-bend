from django.db import models

class Alert(models.Model):
    name = models.CharField(max_length=150, blank=True, verbose_name='Nombre')
    description = models.TextField(max_length=500, blank=True, verbose_name='Descripción')
    is_read = models.BooleanField(default=False, verbose_name='Leído')
    date = models.DateTimeField(auto_now=True, verbose_name='Fecha')

    measurement = models.OneToOneField('api.Measurement', on_delete=models.CASCADE, blank=False, null=False, verbose_name='Medición')
    limit_history = models.ForeignKey('api.LimitHistory', on_delete=models.CASCADE, blank=False, null=False, verbose_name='Historial de límites')

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'alerta'
        ordering = ['-date']
