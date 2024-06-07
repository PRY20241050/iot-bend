from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=50, blank=True, null=True)
    
    brickyard = models.ForeignKey('api.Brickyard', on_delete=models.CASCADE, blank=True, null=True)
    institution = models.ForeignKey('api.Institution', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'auth_user'

    # groups = models.ManyToManyField(
    #     Group,
    #     related_name='customuser_set',  # Cambia related_name para evitar conflictos
    #     blank=True,
    #     help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    #     related_query_name='customuser',
    # )
    # user_permissions = models.ManyToManyField(
    #     Permission,
    #     related_name='customuser_set',  # Cambia related_name para evitar conflictos
    #     blank=True,
    #     help_text='Specific permissions for this user.',
    #     related_query_name='customuser',
    # )
