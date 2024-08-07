# Generated by Django 5.0.6 on 2024-07-19 16:54

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    replaces = [
        ("api", "0002_remove_management_created_at_and_more"),
        ("api", "0003_alter_brickyard_options_alter_institution_options_and_more"),
        ("api", "0004_alter_device_options_alter_device_battery_level_and_more"),
        ("api", "0005_alter_gastype_name"),
        ("api", "0006_alter_gastype_options_gastype_abbreviation"),
        ("api", "0007_alter_sensor_options_remove_measurement_gas_type_and_more"),
        ("api", "0008_rename_status_measurement_measurement_status"),
        ("api", "0009_alter_measurement_options_alter_status_options_and_more"),
        ("api", "0010_alter_emissionlimit_options_and_more"),
        ("api", "0011_alter_measurement_value"),
        ("api", "0012_alter_measurement_value"),
        ("api", "0013_emissionlimit_institution_and_more"),
        ("api", "0014_emissionlimit_is_default"),
        ("api", "0015_measurement_medicion_date_54165f_idx_and_more"),
        ("api", "0016_alter_alert_options_remove_alert_limit_history_and_more"),
    ]

    dependencies = [
        ("api", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="management",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="management",
            name="last_update",
        ),
        migrations.AddField(
            model_name="institution",
            name="brickyards",
            field=models.ManyToManyField(
                through="api.Management", to="api.brickyard", verbose_name="Ladrilleras"
            ),
        ),
        migrations.AlterField(
            model_name="alert",
            name="date",
            field=models.DateTimeField(auto_now=True, verbose_name="Fecha"),
        ),
        migrations.AlterField(
            model_name="alert",
            name="description",
            field=models.TextField(blank=True, max_length=500, verbose_name="Descripción"),
        ),
        migrations.AlterField(
            model_name="alert",
            name="is_read",
            field=models.BooleanField(default=False, verbose_name="Leído"),
        ),
        migrations.AlterField(
            model_name="alert",
            name="limit_history",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="api.limithistory",
                verbose_name="Historial de límites",
            ),
        ),
        migrations.AlterField(
            model_name="alert",
            name="measurement",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to="api.measurement",
                verbose_name="Medición",
            ),
        ),
        migrations.AlterField(
            model_name="alert",
            name="name",
            field=models.CharField(blank=True, max_length=150, verbose_name="Nombre"),
        ),
        migrations.AlterField(
            model_name="brickyard",
            name="address",
            field=models.CharField(blank=True, max_length=200, verbose_name="Dirección"),
        ),
        migrations.AlterField(
            model_name="brickyard",
            name="contact",
            field=models.CharField(blank=True, max_length=100, verbose_name="Contacto"),
        ),
        migrations.AlterField(
            model_name="brickyard",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación"),
        ),
        migrations.AlterField(
            model_name="brickyard",
            name="last_update",
            field=models.DateTimeField(auto_now=True, verbose_name="Última actualización"),
        ),
        migrations.AlterField(
            model_name="brickyard",
            name="name",
            field=models.CharField(blank=True, max_length=150, verbose_name="Nombre"),
        ),
        migrations.AlterField(
            model_name="brickyard",
            name="phone",
            field=models.IntegerField(blank=True, null=True, verbose_name="Teléfono"),
        ),
        migrations.AlterField(
            model_name="brickyard",
            name="ruc",
            field=models.CharField(blank=True, max_length=11, verbose_name="RUC"),
        ),
        migrations.AlterField(
            model_name="device",
            name="battery_level",
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=3,
                verbose_name="Nivel de batería",
            ),
        ),
        migrations.AlterField(
            model_name="device",
            name="brickyard",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="api.brickyard",
                verbose_name="Ladrillera",
            ),
        ),
        migrations.AlterField(
            model_name="device",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación"),
        ),
        migrations.AlterField(
            model_name="device",
            name="description",
            field=models.TextField(blank=True, max_length=500, verbose_name="Descripción"),
        ),
        migrations.AlterField(
            model_name="device",
            name="last_update",
            field=models.DateTimeField(auto_now=True, verbose_name="Última actualización"),
        ),
        migrations.AlterField(
            model_name="device",
            name="name",
            field=models.CharField(blank=True, max_length=100, verbose_name="Nombre"),
        ),
        migrations.AlterField(
            model_name="device",
            name="status",
            field=models.BooleanField(default=False, verbose_name="Estado"),
        ),
        migrations.AlterField(
            model_name="emissionlimit",
            name="app_alert",
            field=models.BooleanField(default=False, verbose_name="Alerta de aplicación"),
        ),
        migrations.AlterField(
            model_name="emissionlimit",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación"),
        ),
        migrations.AlterField(
            model_name="emissionlimit",
            name="description",
            field=models.TextField(blank=True, max_length=250, verbose_name="Descripción"),
        ),
        migrations.AlterField(
            model_name="emissionlimit",
            name="email_alert",
            field=models.BooleanField(default=False, verbose_name="Alerta de correo electrónico"),
        ),
        migrations.AlterField(
            model_name="emissionlimit",
            name="last_update",
            field=models.DateTimeField(auto_now=True, verbose_name="Última actualización"),
        ),
        migrations.AlterField(
            model_name="emissionlimit",
            name="management",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="api.management",
                verbose_name="Administración",
            ),
        ),
        migrations.AlterField(
            model_name="emissionlimit",
            name="name",
            field=models.CharField(blank=True, max_length=100, verbose_name="Nombre"),
        ),
        migrations.AlterField(
            model_name="gastype",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación"),
        ),
        migrations.AlterField(
            model_name="gastype",
            name="last_update",
            field=models.DateTimeField(auto_now=True, verbose_name="Última actualización"),
        ),
        migrations.AlterField(
            model_name="gastype",
            name="name",
            field=models.CharField(max_length=100, verbose_name="Nombre"),
        ),
        migrations.AlterField(
            model_name="institution",
            name="address",
            field=models.CharField(blank=True, max_length=200, verbose_name="Dirección"),
        ),
        migrations.AlterField(
            model_name="institution",
            name="contact",
            field=models.CharField(blank=True, max_length=100, verbose_name="Contacto"),
        ),
        migrations.AlterField(
            model_name="institution",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación"),
        ),
        migrations.AlterField(
            model_name="institution",
            name="last_update",
            field=models.DateTimeField(auto_now=True, verbose_name="Última actualización"),
        ),
        migrations.AlterField(
            model_name="institution",
            name="name",
            field=models.CharField(blank=True, max_length=150, verbose_name="Nombre"),
        ),
        migrations.AlterField(
            model_name="institution",
            name="phone",
            field=models.IntegerField(blank=True, null=True, verbose_name="Teléfono"),
        ),
        migrations.AlterField(
            model_name="limithistory",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación"),
        ),
        migrations.AlterField(
            model_name="limithistory",
            name="emission_limit",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="api.emissionlimit",
                verbose_name="Límite de emisión",
            ),
        ),
        migrations.AlterField(
            model_name="limithistory",
            name="end_date",
            field=models.DateTimeField(blank=True, null=True, verbose_name="Fecha de fin"),
        ),
        migrations.AlterField(
            model_name="limithistory",
            name="gas_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="api.gastype",
                verbose_name="Tipo de gas",
            ),
        ),
        migrations.AlterField(
            model_name="limithistory",
            name="is_modified",
            field=models.BooleanField(default=False, verbose_name="Es modificable"),
        ),
        migrations.AlterField(
            model_name="limithistory",
            name="last_update",
            field=models.DateTimeField(auto_now=True, verbose_name="Última actualización"),
        ),
        migrations.AlterField(
            model_name="limithistory",
            name="max_limit",
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=5, verbose_name="Límite máximo"
            ),
        ),
        migrations.AlterField(
            model_name="limithistory",
            name="start_date",
            field=models.DateTimeField(blank=True, null=True, verbose_name="Fecha de inicio"),
        ),
        migrations.AlterField(
            model_name="management",
            name="brickyard",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="api.brickyard",
                verbose_name="Ladrillera",
            ),
        ),
        migrations.AlterField(
            model_name="management",
            name="institution",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="api.institution",
                verbose_name="Institución",
            ),
        ),
        migrations.AlterField(
            model_name="measurement",
            name="date",
            field=models.DateTimeField(blank=True, null=True, verbose_name="Fecha"),
        ),
        migrations.AlterField(
            model_name="measurement",
            name="sensor",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="api.sensor",
                verbose_name="Sensor",
            ),
        ),
        migrations.AlterField(
            model_name="measurement",
            name="value",
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=5, verbose_name="Valor"
            ),
        ),
        migrations.AlterField(
            model_name="sensor",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación"),
        ),
        migrations.AlterField(
            model_name="sensor",
            name="last_update",
            field=models.DateTimeField(auto_now=True, verbose_name="Última actualización"),
        ),
        migrations.AlterField(
            model_name="status",
            name="name",
            field=models.CharField(max_length=50, verbose_name="Nombre"),
        ),
        migrations.AlterModelOptions(
            name="brickyard",
            options={
                "verbose_name": "Ladrillera",
                "verbose_name_plural": "Ladrilleras",
            },
        ),
        migrations.AlterModelOptions(
            name="institution",
            options={
                "verbose_name": "Institución",
                "verbose_name_plural": "Instituciones",
            },
        ),
        migrations.AlterModelOptions(
            name="management",
            options={
                "verbose_name": "Administración",
                "verbose_name_plural": "Administraciones",
            },
        ),
        migrations.AlterUniqueTogether(
            name="management",
            unique_together={("brickyard", "institution")},
        ),
        migrations.AlterModelOptions(
            name="device",
            options={
                "verbose_name": "Dispositivo",
                "verbose_name_plural": "Dispositivos",
            },
        ),
        migrations.AlterField(
            model_name="device",
            name="battery_level",
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=5,
                verbose_name="Nivel de batería",
            ),
        ),
        migrations.AlterField(
            model_name="device",
            name="status",
            field=models.BooleanField(default=False, verbose_name="Está activado"),
        ),
        migrations.AlterModelOptions(
            name="gastype",
            options={
                "verbose_name": "Tipo de gas",
                "verbose_name_plural": "Tipos de gas",
            },
        ),
        migrations.AddField(
            model_name="gastype",
            name="abbreviation",
            field=models.CharField(default=1, max_length=10, verbose_name="Abreviatura"),
            preserve_default=False,
        ),
        migrations.AlterModelOptions(
            name="sensor",
            options={"verbose_name": "Sensor", "verbose_name_plural": "Sensores"},
        ),
        migrations.RemoveField(
            model_name="measurement",
            name="gas_type",
        ),
        migrations.AddField(
            model_name="measurement",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="Fecha de creación",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="measurement",
            name="status",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="api.status",
                verbose_name="Estado de la lectura",
            ),
        ),
        migrations.AlterModelOptions(
            name="measurement",
            options={"verbose_name": "Medición", "verbose_name_plural": "Mediciones"},
        ),
        migrations.AlterModelOptions(
            name="status",
            options={
                "verbose_name": "Estado de la medición",
                "verbose_name_plural": "Estados de la medición",
            },
        ),
        migrations.AlterModelOptions(
            name="emissionlimit",
            options={
                "verbose_name": "Límite de emisión",
                "verbose_name_plural": "Límites de emisión",
            },
        ),
        migrations.AlterModelOptions(
            name="limithistory",
            options={
                "verbose_name": "Historial de límite",
                "verbose_name_plural": "Historial de límites",
            },
        ),
        migrations.AlterField(
            model_name="emissionlimit",
            name="app_alert",
            field=models.BooleanField(
                default=False,
                help_text="Se enviará una notificación a la aplicación",
                verbose_name="Alerta por aplicación",
            ),
        ),
        migrations.AlterField(
            model_name="emissionlimit",
            name="email_alert",
            field=models.BooleanField(
                default=False,
                help_text="Se enviará una notificación por correo electrónico",
                verbose_name="Alerta por correo electrónico",
            ),
        ),
        migrations.AlterField(
            model_name="limithistory",
            name="max_limit",
            field=models.DecimalField(
                decimal_places=3,
                default=0,
                help_text="Límite máximo permitido en mg x m3",
                max_digits=7,
                verbose_name="Límite máximo",
            ),
        ),
        migrations.AlterField(
            model_name="measurement",
            name="value",
            field=models.DecimalField(
                decimal_places=4,
                default=0,
                help_text="Medido en mg x m3",
                max_digits=9,
                verbose_name="Valor",
            ),
        ),
        migrations.AddField(
            model_name="emissionlimit",
            name="institution",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="api.institution",
                verbose_name="Institución",
            ),
        ),
        migrations.AlterField(
            model_name="emissionlimit",
            name="management",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="api.management",
                verbose_name="Administración",
            ),
        ),
        migrations.AddField(
            model_name="emissionlimit",
            name="is_default",
            field=models.BooleanField(
                default=False,
                help_text="Este límite de emisión es el predeterminado",
                verbose_name="Predeterminado",
            ),
        ),
        migrations.AddIndex(
            model_name="measurement",
            index=models.Index(fields=["date"], name="medicion_date_54165f_idx"),
        ),
        migrations.AddIndex(
            model_name="measurement",
            index=models.Index(fields=["sensor"], name="medicion_sensor__e8d3ee_idx"),
        ),
        migrations.AlterModelOptions(
            name="alert",
            options={
                "ordering": ["-date"],
                "verbose_name": "Alerta",
                "verbose_name_plural": "Alertas",
            },
        ),
        migrations.RemoveField(
            model_name="alert",
            name="limit_history",
        ),
        migrations.RemoveField(
            model_name="alert",
            name="measurement",
        ),
        migrations.AddField(
            model_name="alert",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Usuario",
            ),
            preserve_default=False,
        ),
    ]
