from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField("email address", blank=False, unique=True)
    role = models.CharField(max_length=50, blank=True, default='')
    
    brickyard = models.ForeignKey('api.Brickyard', on_delete=models.CASCADE, blank=True, null=True)
    institution = models.ForeignKey('api.Institution', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'auth_user'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
