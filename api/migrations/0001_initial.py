# Generated by Django 5.0.6 on 2024-06-03 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('description', models.TextField(blank=True, max_length=500)),
                ('status', models.BooleanField(default=False)),
                ('battery_level', models.DecimalField(decimal_places=2, default=0, max_digits=3)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'device',
            },
        ),
    ]
