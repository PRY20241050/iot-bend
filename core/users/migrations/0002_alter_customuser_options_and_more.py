# Generated by Django 5.0.6 on 2024-06-09 01:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'Usuario', 'verbose_name_plural': 'Usuarios'},
        ),
        migrations.RenameField(
            model_name='customuser',
            old_name='user_type',
            new_name='role',
        ),
    ]