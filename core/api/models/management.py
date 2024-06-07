from django.db import models

class Management(models.Model):
    brickyard = models.ForeignKey('api.Brickyard', on_delete=models.CASCADE, blank=False, null=False, verbose_name='Ladrillera')
    institution = models.ForeignKey('api.Institution', on_delete=models.CASCADE, blank=False, null=False, verbose_name='Institución')

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'administracion'
