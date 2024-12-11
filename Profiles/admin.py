from django.contrib import admin
from registration.models import Profile

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','created','trial_month','date_subscription','subscription_month')
    ordering = ('-date_subscription',)

admin.site.register(Profile, ProfileAdmin)
# Configuración del panel de gestion de administrador


