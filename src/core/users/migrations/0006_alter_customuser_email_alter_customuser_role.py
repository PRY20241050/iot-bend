# Generated by Django 5.0.7 on 2024-08-05 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_alter_customuser_options_and_more_squashed_0005_alter_customuser_role"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="email",
            field=models.EmailField(max_length=254, unique=True, verbose_name="Correo electrónico"),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="role",
            field=models.CharField(blank=True, default="", max_length=50, verbose_name="Rol"),
        ),
    ]