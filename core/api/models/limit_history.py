from django.db import models

class LimitHistory(models.Model):
    max_limit = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='Límite máximo')
    start_date = models.DateTimeField(auto_now_add=False, blank=True, null=True, verbose_name='Fecha de inicio')
    end_date = models.DateTimeField(auto_now_add=False, blank=True, null=True, verbose_name='Fecha de fin')
    is_modified = models.BooleanField(default=False, verbose_name='Es modificable')
    
    emission_limit = models.ForeignKey('api.EmissionLimit', on_delete=models.CASCADE, blank=False, null=False, verbose_name='Límite de emisión')
    gas_type = models.ForeignKey('api.GasType', on_delete=models.CASCADE, blank=False, null=False, verbose_name='Tipo de gas')

    last_update = models.DateTimeField(auto_now=True, verbose_name='Última actualización')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    
    def __str__(self):
        return self.value
    
    class Meta:
        db_table = 'historial_limite'
