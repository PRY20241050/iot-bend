from django.db import models

class Management(models.Model):
    institution = models.ForeignKey('api.Institution', on_delete=models.CASCADE, blank=False, null=False, verbose_name='Institución')
    brickyard = models.ForeignKey('api.Brickyard', on_delete=models.CASCADE, blank=False, null=False, verbose_name='Ladrillera')

    def __str__(self):
        return f'{self.institution.name} - {self.brickyard.name}'
    
    class Meta:
        db_table = 'administracion'
        verbose_name = 'Administración'
        verbose_name_plural = 'Administraciones'
        unique_together = ('brickyard', 'institution')
