# Generated by Django 5.0.7 on 2024-08-11 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0021_rename_last_update_emissionlimit_updated_at_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="gastype",
            old_name="last_update",
            new_name="updated_at",
        ),
        migrations.RenameField(
            model_name="institution",
            old_name="last_update",
            new_name="updated_at",
        ),
        migrations.RenameField(
            model_name="limithistory",
            old_name="last_update",
            new_name="updated_at",
        ),
        migrations.RenameField(
            model_name="sensor",
            old_name="last_update",
            new_name="updated_at",
        ),
    ]
