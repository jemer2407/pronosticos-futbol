# Generated by Django 5.1.3 on 2024-12-10 09:22

import django.db.models.deletion
import registration.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=registration.models.custom_upload_to, verbose_name='Imagen de perfil')),
                ('bio', models.TextField(blank=True, null=True, verbose_name='Biografía')),
                ('link', models.URLField(blank=True, null=True, verbose_name='Enlace')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha creación perfil')),
                ('trial_month', models.DateTimeField(verbose_name='Fecha final de prueba')),
                ('date_subscription', models.DateTimeField(blank=True, null=True, verbose_name='Fecha suscripción')),
                ('subscription_month', models.DateTimeField(blank=True, null=True, verbose_name='Fecha final suscripción')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user__username'],
            },
        ),
    ]