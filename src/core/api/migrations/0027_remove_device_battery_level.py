# Generated by Django 5.0.7 on 2024-09-09 04:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0026_alter_device_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="device",
            name="battery_level",
        ),
    ]
