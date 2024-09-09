# Generated by Django 5.0.7 on 2024-09-09 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0023_remove_emissionlimit_is_default_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="brickyard",
            name="address",
            field=models.CharField(max_length=200, verbose_name="Dirección"),
        ),
        migrations.AlterField(
            model_name="brickyard",
            name="name",
            field=models.CharField(max_length=150, verbose_name="Nombre"),
        ),
        migrations.AlterField(
            model_name="brickyard",
            name="ruc",
            field=models.CharField(max_length=11, verbose_name="RUC"),
        ),
    ]
