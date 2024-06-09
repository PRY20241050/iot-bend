from django.db import models

class Institution(models.Model):
    name = models.CharField(max_length=150, blank=True, verbose_name='Nombre')
    address = models.CharField(max_length=200, blank=True, verbose_name='Dirección')
    phone = models.IntegerField(blank=True, null=True, verbose_name='Teléfono')
    contact = models.CharField(max_length=100, blank=True, verbose_name='Contacto')
    
    brickyards = models.ManyToManyField('api.Brickyard', through='api.Management', verbose_name='Ladrilleras')
    
    last_update = models.DateTimeField(auto_now=True, verbose_name='Última actualización')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'institucion'
        verbose_name = 'Institución'
        verbose_name_plural = 'Instituciones'
