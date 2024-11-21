from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
import numpy as np
from .models import Match


# ----------- funciones para calcular los diferentes mercados -----------------
# funcion para obtener todos los partidos jugados de ambos equipos tanto como de local como de visitante
def get_matches_both_team(obj):
    matches = []# lista para almacenar todos los partidos jugados de los dos equipos tanto como de local como de visitante
    # Obtener estadísticas de los equipos
    # local como local partidos jugados
    home_home = Match.objects.filter(home_team=obj.home_team).filter(gol_home_ht__gt=-1)
    matches.append(home_home)
    # local como visitante partidos jugados
    home_visit = Match.objects.filter(visit_team=obj.home_team).filter(gol_home_ht__gt=-1)
    matches.append(home_visit)
    # visitante como local partidos jugados
    visit_home = Match.objects.filter(home_team=obj.visit_team).filter(gol_home_ht__gt=-1)
    matches.append(visit_home)
    # visitante como visitante partidos jugados
    visit_visit = Match.objects.filter(visit_team=obj.visit_team).filter(gol_home_ht__gt=-1)
    matches.append(visit_visit)
    num_match_over_05_ht = 0
    num_match_over_15_ht = 0
    num_match_over_05_ft = 0
    num_match_over_15_ft = 0
    num_match_over_25_ft = 0
    total_matches = 0
    for m in matches:#iteramos la lista de partidos y llamamos a la funcion que nos calcula el numero de partidos over 0.5 ht
        num_match_over_05_ht += calcular_over(m, 0, 'ht')
        num_match_over_15_ht += calcular_over(m, 1, 'ht')
        num_match_over_05_ft += calcular_over(m, 0, 'ft')
        num_match_over_15_ft += calcular_over(m, 1, 'ft')
        num_match_over_25_ft += calcular_over(m, 2, 'ft')
        total_matches += len(m)

    return total_matches, num_match_over_05_ht, num_match_over_15_ht, num_match_over_05_ft, num_match_over_15_ft, num_match_over_25_ft

# funcion over ht
def calcular_over(m, goles, tiempo):
    num_match_over = 0    
    for match in m:
        if tiempo == 'ht':
            if match.gol_home_ht + match.gol_visit_ht > goles:
                num_match_over += 1
        else:
            if match.gol_home_ft + match.gol_visit_ft > goles:
                num_match_over += 1
    
    return num_match_over



















# Create your views here.

class NextMatchesListView(ListView):
    model = Match
    template_name = 'forecasts/matches_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Próximos partidos'
        return context
    
    def get_queryset(self):
        unplayed_match = Match.objects.filter(gol_home_ht=None)  # aqui obtengo los que no se han jugado aun
        ten_matches = unplayed_match[:10]
        
        return ten_matches


class MatchDetailView(DetailView):
    model = Match
    template_name = 'forecasts/match_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Pronosticos del '

        # lógica para calcular las probabilidades de los diferentes mercados
        # ------------------------------------ over ht y ft ----------------------------------------
        total_matches, num_match_over_05_ht, num_match_over_15_ht, num_match_over_05_ft, num_match_over_15_ft, num_match_over_25_ft = get_matches_both_team(self.get_object())
        prob_over_05_ht = np.round(100 * num_match_over_05_ht / total_matches,2)
        prob_over_15_ht = np.round(100 * num_match_over_15_ht / total_matches,2)
        prob_over_05_ft = np.round(100 * num_match_over_05_ft / total_matches,2)
        prob_over_15_ft = np.round(100 * num_match_over_15_ft / total_matches,2)
        prob_over_25_ft = np.round(100 * num_match_over_25_ft / total_matches,2)


        context['prob_over_05_ht'] = prob_over_05_ht
        context['cuota_over_05_ht'] = np.round((1/prob_over_05_ht)*100,2)
        context['prob_over_15_ht'] = prob_over_15_ht
        context['cuota_over_15_ht'] = np.round((1/prob_over_15_ht)*100,2)

        context['prob_over_05_ft'] = prob_over_05_ft
        context['cuota_over_05_ft'] = np.round((1/prob_over_05_ft)*100,2)
        context['prob_over_15_ft'] = prob_over_15_ft
        context['cuota_over_15_ft'] = np.round((1/prob_over_15_ft)*100,2)
        context['prob_over_25_ft'] = prob_over_25_ft
        context['cuota_over_25_ft'] = np.round((1/prob_over_25_ft)*100,2)

        # ----------------------

        return context