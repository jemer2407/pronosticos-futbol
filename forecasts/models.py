from django.db import models


# Create your models here. 
# year.strftime('%Y')
#{{ year|date: "Y" }}
# modelo temporada
class Season(models.Model):
    season = models.DateField(verbose_name='Temporada')

    class Meta:
        verbose_name = 'Temporada'
        verbose_name_plural = 'Temporadas'

    def __str__(self):
        return self.season.strftime('%Y')

class Contry(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre')

    class Meta:
        verbose_name = 'Pais'
        verbose_name_plural = 'Paises'
        
    def __str__(self):
        return self.name

class League(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')
    season = models.ForeignKey(Season, on_delete=models.CASCADE, blank=False, null=False, verbose_name='Temporada')
    contry = models.ForeignKey(Contry, on_delete=models.CASCADE, blank=False, null=False, verbose_name='Pais')

    class Meta:
        verbose_name = 'Liga'
        verbose_name_plural = 'Ligas'
        ordering = ['name']
        
    
    def __str__(self):
        return self.name

class Team(models.Model):
    team = models.CharField(max_length=50, verbose_name='Equipo')
    league = models.ForeignKey(League, on_delete=models.CASCADE, blank=False, null=False, verbose_name='Liga')
    image = models.ImageField(verbose_name='Imagen', upload_to='team')
    class Meta:
        verbose_name = 'Equipo'
        verbose_name_plural = 'Equipos'
        ordering = ['team']
        
    
    def __str__(self):
        return self.team


class Match(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE, blank=False, null=False, verbose_name='Liga')
    soccer_day = models.SmallIntegerField(verbose_name='Jornada', null=True, blank=True)
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=False, null=False, verbose_name='Equipo local',related_name='home_matches')
    visit_team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=False, null=False, verbose_name='Equipo visitante',related_name='visit_matches')
    date = models.DateField(verbose_name='Fecha')
    gol_home_ht = models.IntegerField(verbose_name='Goles Equipo Local HT', blank=True, null=True)
    gol_visit_ht = models.IntegerField(verbose_name='Goles Equipo Visitante HT', blank=True, null=True)
    gol_home_ft = models.IntegerField(verbose_name='Goles Equipo Local FT', blank=True, null=True)
    gol_visit_ft = models.IntegerField(verbose_name='Goles Equipo Visitante FT', blank=True, null=True)

    class Meta:
        verbose_name = 'Partido'
        verbose_name_plural = 'Partidos'
        ordering = ['league']
        
    
    def __str__(self):
        return '{} {}'.format(self.home_team, self.visit_team)