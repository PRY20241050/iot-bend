from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

# class CustomUser(AbstractUser):
#     bio = models.TextField(max_length=500, blank=True, null=True)
#     user_type = models.CharField(max_length=50, blank=True, null=True)

#     groups = models.ManyToManyField(
#         Group,
#         related_name='customuser_set',  # Cambia related_name para evitar conflictos
#         blank=True,
#         help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
#         related_query_name='customuser',
#     )
#     user_permissions = models.ManyToManyField(
#         Permission,
#         related_name='customuser_set',  # Cambia related_name para evitar conflictos
#         blank=True,
#         help_text='Specific permissions for this user.',
#         related_query_name='customuser',
#     )
