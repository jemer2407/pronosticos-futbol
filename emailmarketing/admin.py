from django.contrib import admin
from .models import Subscriber


# Register your models here.
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email',)
    ordering = ('-email',)

admin.site.register(Subscriber, SubscriberAdmin)

# Configuración del panel de gestion de administrador
title = "Administrador Email Marketing"
subtitle = 'Panel de gestión'
admin.site.site_header = title
admin.site.site_title = title
admin.site.index_title = subtitle