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
    num_total_match_home_home,num_match_win_home_home, num_match_lose_home_home, num_match_empate_home_home = calcular_num_match_1x2(home_home, 'home_home')
    num_total_match_home_visit,num_match_win_home_visit, num_match_lose_home_visit, num_match_empate_home_visit = calcular_num_match_1x2(home_visit, 'home_visit')
    num_total_match_visit_home,num_match_win_visit_home, num_match_lose_visit_home, num_match_empate_visit_home = calcular_num_match_1x2(visit_home, 'visit_home')
    num_total_match_visit_visit,num_match_win_visit_visit, num_match_lose_visit_visit, num_match_empate_visit_visit = calcular_num_match_1x2(visit_visit, 'visit_visit')
    
    # calculamos numero de partidos gana,pierde y empata local_local, local_visitante, visitante_local, visitante_visitante
    # numero de partidos para gana local
    
    num_total_match_win_home = num_match_win_home_home + num_match_win_home_visit# numero de partidos que ha ganado el local
    num_total_match_lose_visit = num_match_lose_visit_home + num_match_lose_visit_visit# numero de partidos que ha perdido el visitante
    

    # numero de partidos para gana visitante
    num_total_match_win_visit = num_match_win_visit_home + num_match_win_visit_visit
    num_total_match_lose_home = num_match_lose_home_home + num_match_lose_home_visit


    num_total_match_empate_home = num_match_empate_home_home + num_match_empate_home_visit
    num_total_match_empate_visit = num_match_empate_visit_home + num_match_empate_visit_visit

    num_total_match_home = num_total_match_home_home + num_total_match_home_visit# numero total de partidos que ha jugado el local
    num_total_match_visit = num_total_match_visit_home + num_total_match_visit_visit# numero total de partidos que ha jugado el visitante

    
    num_match_over_05_ht = 0
    num_match_over_15_ht = 0
    num_match_over_05_ft = 0
    num_match_over_15_ft = 0
    num_match_over_25_ft = 0
    num_match_over_35_ft = 0
    num_match_over_05_mitad2 = 0
    num_match_aem_ft = 0
    num_match_aem_ht = 0
    num_match_aem_ht2 = 0
    
    total_matches = 0
    for m in matches:#iteramos la lista de partidos y llamamos a la funcion que nos calcula el numero de partidos over 0.5 ht
        num_match_over_05_ht += calcular_prob_over(m, 0, 'ht')
        num_match_over_15_ht += calcular_prob_over(m, 1, 'ht')
        num_match_over_05_ft += calcular_prob_over(m, 0, 'ft')
        num_match_over_15_ft += calcular_prob_over(m, 1, 'ft')
        num_match_over_25_ft += calcular_prob_over(m, 2, 'ft')
        num_match_over_35_ft += calcular_prob_over(m, 3, 'ft')
        num_match_over_05_mitad2 += calcular_prob_over(m,0,'ht2')
        num_match_aem_ft += calcular_prob_aem(m,'ft')
        num_match_aem_ht += calcular_prob_aem(m,'ht')
        num_match_aem_ht2 += calcular_prob_aem(m,'ht2')
        
        total_matches += len(m)

    return total_matches,num_match_over_05_ht,num_match_over_15_ht,num_match_over_05_ft,num_match_over_15_ft,num_match_over_25_ft,num_match_over_35_ft,num_match_over_05_mitad2,num_match_aem_ft,num_match_aem_ht,num_match_aem_ht2,num_total_match_win_home,num_total_match_lose_visit,num_total_match_win_visit,num_total_match_lose_home,num_total_match_empate_home,num_total_match_empate_visit,num_total_match_home,num_total_match_visit
        

# funcion que calcula el numero de partidos que se ha dado el over
def calcular_prob_over(m, goles, tiempo):
    num_match_over = 0    
    for match in m:
        if tiempo == 'ht':
            if match.gol_home_ht + match.gol_visit_ht > goles:
                num_match_over += 1
        elif tiempo == 'ft':
            if match.gol_home_ft + match.gol_visit_ft > goles:
                num_match_over += 1
        elif tiempo == 'ht2':
            if (match.gol_home_ft - match.gol_home_ht) + (match.gol_visit_ft - match.gol_visit_ht) > goles:
                num_match_over += 1
    
    return num_match_over


# funcion que calcula el numero de partidos que se ha dado el aem
def calcular_prob_aem(m,tiempo):
    num_match_aem = 0
    for match in m:
        if tiempo == 'ft':
            if match.gol_home_ft > 0 and match.gol_visit_ft > 0:
                num_match_aem += 1
        if tiempo == 'ht':
            if match.gol_home_ht > 0 and match.gol_visit_ht > 0:
                num_match_aem += 1
        if tiempo == 'ht2':
            if (match.gol_home_ft - match.gol_home_ht) > 0 and (match.gol_visit_ft - match.gol_visit_ht) > 0:
                num_match_aem += 1

    return num_match_aem        

# funcion que calcula el numero de partidos que se ha dado el gana local, empate y gana visitante
def calcular_num_match_1x2(m, option):
    num_match_win = 0
    num_match_lose = 0
    num_match_empate = 0
    num_total_match_1x2 = 0
    
    for match in m:
        if option == 'home_home':
            if match.gol_home_ft > match.gol_visit_ft:
                num_match_win += 1
            if match.gol_home_ft < match.gol_visit_ft:
                num_match_lose += 1
            if match.gol_home_ft == match.gol_visit_ft:
                num_match_empate += 1

        if option == 'home_visit':
            if match.gol_visit_ft > match.gol_home_ft:
                num_match_win += 1
            if match.gol_visit_ft < match.gol_home_ft:
                num_match_lose += 1
            if match.gol_visit_ft == match.gol_home_ft:
                num_match_empate += 1

        if option == 'visit_home':
            if match.gol_home_ft > match.gol_visit_ft:
                num_match_win += 1
            if match.gol_home_ft < match.gol_visit_ft:
                num_match_lose += 1
            if match.gol_home_ft == match.gol_visit_ft:
                num_match_empate += 1
            
        if option == 'visit_visit':
            if match.gol_visit_ft > match.gol_home_ft:
                num_match_win += 1
            if match.gol_visit_ft < match.gol_home_ft:
                num_match_lose += 1
            if match.gol_visit_ft == match.gol_home_ft:
                num_match_empate += 1
        num_total_match_1x2 += 1
        # 
    
    return num_total_match_1x2, num_match_win,num_match_lose,num_match_empate


# --------------------------- Create your views here ------------------------------

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
        context['title'] = 'Pronósticos para     '

        # lógica para calcular las probabilidades de los diferentes mercados
        # ------------------------------------ over ht y ft ----------------------------------------
        
        total_matches, num_match_over_05_ht, num_match_over_15_ht, num_match_over_05_ft, num_match_over_15_ft, num_match_over_25_ft, num_match_over_35_ft, num_match_over_05_mitad2, num_match_aem_ft, num_match_aem_ht, num_match_aem_ht2,num_total_match_win_home,num_total_match_lose_visit,num_total_match_win_visit,num_total_match_lose_home,num_total_match_empate_home,num_total_match_empate_visit,num_total_match_home,num_total_match_visit = get_matches_both_team(self.get_object())
            
            
        prob_over_05_ht = np.round(100 * num_match_over_05_ht / total_matches,2)
        prob_over_15_ht = np.round(100 * num_match_over_15_ht / total_matches,2)
        prob_over_05_ft = np.round(100 * num_match_over_05_ft / total_matches,2)
        prob_over_15_ft = np.round(100 * num_match_over_15_ft / total_matches,2)
        prob_over_25_ft = np.round(100 * num_match_over_25_ft / total_matches,2)
        prob_over_35_ft = np.round(100 * num_match_over_35_ft / total_matches,2)
        prob_over_05_mitad2 = np.round(100 * num_match_over_05_mitad2 / total_matches,2)
        prob_aem_ft = np.round(100 * num_match_aem_ft / total_matches,2)
        prob_aem_ht = np.round(100 * num_match_aem_ht / total_matches,2)
        prob_aem_ht2 = np.round(100 * num_match_aem_ht2 / total_matches,2)

        # corregir --> numero de partidos total jugados si ha jugado cada equipo

        prob_win_home = (np.round(100 * num_total_match_win_home / num_total_match_home, 2) + np.round(100 * num_total_match_lose_visit / num_total_match_visit, 2))/2
        prob_win_visit = (np.round(100 * num_total_match_win_visit / num_total_match_visit, 2) + np.round(100 * num_total_match_lose_home / num_total_match_home, 2))/2
        prob_empate = (np.round(100 * num_total_match_empate_home / num_total_match_home, 2) + np.round(100 * num_total_match_empate_visit / num_total_match_visit, 2))/2

        context['prob_win_home'] = round(prob_win_home,2)
        context['cuota_win_home'] = np.round((1/prob_win_home)*100,2)
        context['prob_win_visit'] = round(prob_win_visit,2)
        context['cuota_win_visit'] = np.round((1/prob_win_visit)*100,2)
        context['prob_empate'] = round(prob_empate,2)
        context['cuota_empate'] = np.round((1/prob_empate)*100,2)

        context['prob_over_05_ht'] = round(prob_over_05_ht,2)
        context['cuota_over_05_ht'] = np.round((1/prob_over_05_ht)*100,2)
        context['prob_under_05_ht'] = round(100-prob_over_05_ht,2)
        context['cuota_under_05_ht'] = np.round((1/(100 - prob_over_05_ht))*100,2)

        context['prob_over_15_ht'] = round(prob_over_15_ht,2)
        context['cuota_over_15_ht'] = np.round((1/prob_over_15_ht)*100,2)
        context['prob_under_15_ht'] = round(100 - prob_over_15_ht,2)
        context['cuota_under_15_ht'] = np.round((1/(100 - prob_over_15_ht))*100,2)

        context['prob_over_05_ft'] = round(prob_over_05_ft,2)
        context['cuota_over_05_ft'] = np.round((1/prob_over_05_ft)*100,2)
        context['prob_under_05_ft'] = round(100-prob_over_05_ft,2)
        context['cuota_under_05_ft'] = np.round((1/(100 - prob_over_05_ft))*100,2)

        context['prob_over_15_ft'] = round(prob_over_15_ft,2)
        context['cuota_over_15_ft'] = np.round((1/prob_over_15_ft)*100,2)
        context['prob_under_15_ft'] = round(100 - prob_over_15_ft,2)
        context['cuota_under_15_ft'] = np.round((1/(100 - prob_over_15_ft))*100,2)

        context['prob_over_25_ft'] = round(prob_over_25_ft,2)
        context['cuota_over_25_ft'] = np.round((1/prob_over_25_ft)*100,2)
        context['prob_under_25_ft'] = round(100 - prob_over_25_ft,2)
        context['cuota_under_25_ft'] = np.round((1/(100 - prob_over_25_ft))*100,2)

        context['prob_over_35_ft'] = round(prob_over_35_ft,2)
        context['cuota_over_35_ft'] = np.round((1/prob_over_35_ft)*100,2)
        context['prob_under_35_ft'] = round(100 - prob_over_35_ft,2)
        context['cuota_under_35_ft'] = np.round((1/(100 - prob_over_35_ft))*100,2)

        context['prob_over_05_mitad2'] = round(prob_over_05_mitad2,2)
        context['cuota_over_05_mitad2'] = np.round((1/prob_over_05_mitad2)*100,2)
        context['prob_under_05_mitad2'] = round(100 - prob_over_05_mitad2,2)
        context['cuota_under_05_mitad2'] = np.round((1/(100 - prob_over_05_mitad2))*100,2)

        context['prob_aem_ft'] = round(prob_aem_ft,2)
        context['cuota_aem_ft'] = np.round((1/prob_aem_ft)*100,2)
        context['prob_aem_ft_no'] = round(100 - prob_aem_ft,2)
        context['cuota_aem_ft_no'] = np.round((1/(100 - prob_aem_ft))*100,2)

        context['prob_aem_ht'] = round(prob_aem_ht,2)
        context['cuota_aem_ht'] = np.round((1/prob_aem_ht)*100,2)
        context['prob_aem_ht_no'] = round(100 - prob_aem_ht,2)
        context['cuota_aem_ht_no'] = np.round((1/(100 - prob_aem_ht))*100,2)

        context['prob_aem_ht2'] = round(prob_aem_ht2,2)
        context['cuota_aem_ht2'] = np.round((1/prob_aem_ht2)*100,2)
        context['prob_aem_h2t_no'] = round(100 - prob_aem_ht2,2)
        context['cuota_aem_ht2_no'] = np.round((1/(100 - prob_aem_ht2))*100,2)



       


        return context