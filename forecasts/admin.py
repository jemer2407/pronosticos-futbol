from django.contrib import admin
from .models import Season, Contry, League, Team, Match

# Register your models here.
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('season',)

class ContryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name','season','contry')

class TeamAdmin(admin.ModelAdmin):
    list_display = ('team','league')

class MatchAdmin(admin.ModelAdmin):
    list_display = ('league', 'soccer_day','home_team', 'visit_team', 'date', 'gol_home_ht', 'gol_visit_ht', 'gol_home_ft', 'gol_visit_ft')
    ordering = ('date',)



admin.site.register(Season, SeasonAdmin)
admin.site.register(Contry, ContryAdmin)
admin.site.register(League, LeagueAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Match, MatchAdmin)

# Configuración del panel de gestion de administrador
title = "Proyecto Pronósticos Fútbol"
subtitle = 'Panel de gestión'
admin.site.site_header = title
admin.site.site_title = title
admin.site.index_title = subtitle