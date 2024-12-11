from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import Http404, JsonResponse
import numpy as np
from django.contrib import messages
from .models import Match, League, Strategy
from .forms import MatchesForm, StrategyForm

def calcular_prob(total_matches,
                  num_match_over_05_ht,
                  num_match_over_15_ht,
                  num_match_over_05_ft,
                  num_match_over_15_ft,
                  num_match_over_25_ft,
                  num_match_over_35_ft,
                  num_match_over_05_mitad2,
                  num_match_aem_ft,
                  num_match_aem_ht,
                  num_match_aem_ht2,
                  num_total_match_win_home,
                  num_total_match_home,
                  num_total_match_lose_visit,
                  num_total_match_visit,
                  num_total_match_win_visit,
                  num_total_match_lose_home,
                  num_total_match_empate_home,
                  num_total_match_empate_visit):

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

    
    prob_win_home = (np.round(100 * num_total_match_win_home / num_total_match_home, 2) + np.round(100 * num_total_match_lose_visit / num_total_match_visit, 2))/2
    prob_win_visit = (np.round(100 * num_total_match_win_visit / num_total_match_visit, 2) + np.round(100 * num_total_match_lose_home / num_total_match_home, 2))/2
    prob_empate = (np.round(100 * num_total_match_empate_home / num_total_match_home, 2) + np.round(100 * num_total_match_empate_visit / num_total_match_visit, 2))/2

    return (
        prob_over_05_ht,
        prob_over_15_ht,
        prob_over_05_ft,
        prob_over_15_ft,
        prob_over_25_ft,
        prob_over_35_ft,
        prob_over_05_mitad2,
        prob_aem_ft,
        prob_aem_ht,
        prob_aem_ht2,
        prob_win_home,
        prob_win_visit,
        prob_empate
    )



def calcular_prob_anota_concede_gol(num_total_match,matches_anota_ft,matches_anota_ht,matches_anota_2ht,matches_concede_ft,matches_concede_ht,matches_concede_2ht):

    prob_local_anota_ft = np.round(100 * matches_anota_ft / num_total_match,2)
    prob_local_anota_ht = np.round(100 * matches_anota_ht / num_total_match,2)
    prob_local_anota_2ht = np.round(100 * matches_anota_2ht / num_total_match,2)
    prob_local_concede_ft = np.round(100 * matches_concede_ft / num_total_match,2)
    prob_local_concede_ht = np.round(100 * matches_concede_ht / num_total_match,2)
    prob_local_concede_2ht = np.round(100 * matches_concede_2ht / num_total_match,2)

    return (prob_local_anota_ft,
            prob_local_anota_ht,
            prob_local_anota_2ht,
            prob_local_concede_ft,
            prob_local_concede_ht,
            prob_local_concede_2ht)

# funcion que obtiene el numero de partidos que anota y concede un equipo tanto en ft, ht como 2ht
def get_matches_home_anota_concede_gol(home_home,home_visit):

    matches_anota_ft = 0
    matches_anota_ht = 0
    matches_anota_2ht = 0
    matches_concede_ft = 0
    matches_concede_ht = 0
    matches_concede_2ht = 0

    for match in home_home:
        if match.gol_home_ft > 0:
            matches_anota_ft += 1
        if match.gol_home_ht > 0:
            matches_anota_ht += 1
        if match.gol_home_ft - match.gol_home_ht > 0:
            matches_anota_2ht += 1
        if match.gol_visit_ft > 0:
            matches_concede_ft += 1
        if match.gol_visit_ht > 0:
            matches_concede_ht += 1
        if match.gol_visit_ft - match.gol_visit_ht > 0:
            matches_concede_2ht += 1

    return matches_anota_ft,matches_anota_ht,matches_anota_2ht,matches_concede_ft,matches_concede_ht,matches_concede_2ht




# funcion para obtener todos los partidos jugados de ambos equipos tanto de local como de visitante
def get_matches_home_visit(obj):
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

    return home_home,home_visit,visit_home,visit_visit,matches



# ----------- funciones para calcular los diferentes mercados -----------------

def get_matches_both_team(obj):

    home_home,home_visit,visit_home,visit_visit,matches = get_matches_home_visit(obj)
    
    (num_total_match_home_home, 
     num_match_win_home_home, 
     num_match_lose_home_home, 
     num_match_empate_home_home) = calcular_num_match_1x2(home_home, 'home_home')
    
    (num_total_match_home_visit, 
     num_match_win_home_visit, 
     num_match_lose_home_visit, 
     num_match_empate_home_visit) = calcular_num_match_1x2(home_visit, 'home_visit')
    
    (num_total_match_visit_home, 
     num_match_win_visit_home, 
     num_match_lose_visit_home, 
     num_match_empate_visit_home) = calcular_num_match_1x2(visit_home, 'visit_home')
    
    (num_total_match_visit_visit, 
     num_match_win_visit_visit, 
     num_match_lose_visit_visit, 
     num_match_empate_visit_visit) = calcular_num_match_1x2(visit_visit, 'visit_visit')
    
    # calculamos numero de partidos gana,pierde y empata local_local, local_visitante, visitante_local, visitante_visitante
    # numero de partidos para gana local
    
    num_total_match_win_home = num_match_win_home_home + num_match_win_home_visit# numero de partidos que ha ganado el local
    num_total_match_lose_visit = num_match_lose_visit_home + num_match_lose_visit_visit# numero de partidos que ha perdido el visitante
    

    # numero de partidos para gana visitante
    num_total_match_win_visit = num_match_win_visit_home + num_match_win_visit_visit
    num_total_match_lose_home = num_match_lose_home_home + num_match_lose_home_visit

    # numero de partidos para empate
    num_total_match_empate_home = num_match_empate_home_home + num_match_empate_home_visit
    num_total_match_empate_visit = num_match_empate_visit_home + num_match_empate_visit_visit

    num_total_match_home = num_total_match_home_home + num_total_match_home_visit# numero total de partidos que ha jugado el local
    num_total_match_visit = num_total_match_visit_home + num_total_match_visit_visit# numero total de partidos que ha jugado el visitante
    # -------------------------------------------------------------------------------------
    # numero de partidos que anotan y conceden tanto en ft, ht como 2ht
    (matches_anota_ft,
     matches_anota_ht,
     matches_anota_2ht,
     matches_concede_ft,
     matches_concede_ht,
     matches_concede_2ht) = get_matches_home_anota_concede_gol(home_home,home_visit)
    
    (prob_local_anota_ft,
     prob_local_anota_ht,
     prob_local_anota_2ht,
     prob_local_concede_ft,
     prob_local_concede_ht,
     prob_local_concede_2ht) = calcular_prob_anota_concede_gol(num_total_match_home,
                                                               matches_anota_ft,
                                                               matches_anota_ht,
                                                               matches_anota_2ht,
                                                               matches_concede_ft,
                                                               matches_concede_ht,
                                                               matches_concede_2ht)
    
    (matches_anota_ft,
     matches_anota_ht,
     matches_anota_2ht,
     matches_concede_ft,
     matches_concede_ht,
     matches_concede_2ht) = get_matches_home_anota_concede_gol(visit_home,visit_visit)
    
    (prob_visitante_anota_ft,
     prob_visitante_anota_ht,
     prob_visitante_anota_2ht,
     prob_visitante_concede_ft,
     prob_visitante_concede_ht,
     prob_visitante_concede_2ht) = calcular_prob_anota_concede_gol(num_total_match_visit,
                                                                   matches_anota_ft,
                                                                   matches_anota_ht,
                                                                   matches_anota_2ht,
                                                                   matches_concede_ft,
                                                                   matches_concede_ht,
                                                                   matches_concede_2ht)
    # over y aem --------------------------------------------------------
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
    for m in matches:#iteramos la lista de partidos y llamamos a la funcion que nos calcula el numero de partidos over
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
    # -------------------------------------------------------------------
    return (total_matches,
            num_match_over_05_ht,
            num_match_over_15_ht,
            num_match_over_05_ft,
            num_match_over_15_ft,
            num_match_over_25_ft,
            num_match_over_35_ft,
            num_match_over_05_mitad2,
            num_match_aem_ft,
            num_match_aem_ht,
            num_match_aem_ht2,
            num_total_match_win_home,
            num_total_match_lose_visit,
            num_total_match_win_visit,
            num_total_match_lose_home,
            num_total_match_empate_home,
            num_total_match_empate_visit,
            num_total_match_home,
            num_total_match_visit,
            prob_local_anota_ft,
            prob_local_anota_ht,
            prob_local_anota_2ht,
            prob_local_concede_ft,
            prob_local_concede_ht,
            prob_local_concede_2ht,
            prob_visitante_anota_ft,
            prob_visitante_anota_ht,
            prob_visitante_anota_2ht,
            prob_visitante_concede_ft,
            prob_visitante_concede_ht,
            prob_visitante_concede_2ht)
        

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
        
    
    return num_total_match_1x2, num_match_win,num_match_lose,num_match_empate

def get_next_matches_league(unplayed_matches):
    matches = []
        
    for unplayed_match in unplayed_matches:
        encontrado = False
        if len(matches) != 0:
            for match in matches:
                if unplayed_match.home_team == match.home_team or unplayed_match.home_team == match.visit_team:
                    encontrado = True
                    #print('entra primer if')
                elif unplayed_match.visit_team == match.home_team or unplayed_match.visit_team == match.visit_team: 
                    encontrado = True
                    #print('entra segundo if')

            if encontrado == False:
                #print('encontrado es false')        
                matches.append(unplayed_match)
        else:    
            matches.append(unplayed_match)

    return matches

# funcion que calcula probabilidad de mas de 1, 2 ó 3 goles en el segundo tiempo teniendo en cuenta el resultado al descanso
def calcula_over_2mitad(matches, goles_descanso, goles):
    
    num_total_partidos = 0
    num_partidos_over = 0
    # recorremos la lista de listas de partidos
    
    for match in matches:
        for m in match:
            # comprobamos si el número de goles al descanso es igual al numero de goles pasado por referencia
            if (m.gol_home_ht + m.gol_visit_ht) == goles_descanso:
                print('entra con {} goles'.format(m.gol_home_ht + m.gol_visit_ht))
                num_total_partidos += 1
                if (m.gol_home_ft + m.gol_visit_ft) - (m.gol_home_ht + m.gol_visit_ht) > goles:
                    num_partidos_over += 1
    return num_total_partidos, num_partidos_over


# funcion que devuelve la probabilidad de mas de 1, 2 ó 3 goles en el segundo tiempo teniendo en cuenta el resultado al descanso
def get_prob_goles_2ht_live(goles_descanso,obj):
    print(obj)
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

    num_total_match_un_gol_mas,num_match_un_gol_mas = calcula_over_2mitad(matches, goles_descanso, 0)
    num_total_match_dos_goles_mas,num_match_dos_goles_mas = calcula_over_2mitad(matches, goles_descanso, 1)
    num_total_match_tres_goles_mas,num_match_tres_goles_mas = calcula_over_2mitad(matches, goles_descanso, 2)
    
    if num_total_match_un_gol_mas != 0:
        prob_un_gol_mas = np.round(100 * num_match_un_gol_mas / num_total_match_un_gol_mas, 2)
    else:
        prob_un_gol_mas = 0
    if num_total_match_dos_goles_mas != 0:
        prob_dos_goles_mas = np.round(100 * num_match_dos_goles_mas / num_total_match_dos_goles_mas, 2)
    else:
        prob_dos_goles_mas = 0
    if num_total_match_tres_goles_mas != 0:
        prob_tres_goles_mas = np.round(100 * num_match_tres_goles_mas / num_total_match_tres_goles_mas, 2)
    else:
        prob_tres_goles_mas = 0
    
    return prob_un_gol_mas, prob_dos_goles_mas, prob_tres_goles_mas

# función que devuelve una lista de objetos de partidos que cumplen las condiciones de la estrategia
def get_matches_strategy(matches,strategy):
    strategy_user = Strategy.objects.get(id=strategy)
    matches_strategy = []
    
    for match in matches:
        cumple = True
        (total_matches,
        num_match_over_05_ht,
        num_match_over_15_ht,
        num_match_over_05_ft,
        num_match_over_15_ft,
        num_match_over_25_ft,
        num_match_over_35_ft,
        num_match_over_05_mitad2,
        num_match_aem_ft,
        num_match_aem_ht,
        num_match_aem_ht2,
        num_total_match_win_home,
        num_total_match_lose_visit,
        num_total_match_win_visit,
        num_total_match_lose_home,
        num_total_match_empate_home,
        num_total_match_empate_visit,
        num_total_match_home,
        num_total_match_visit,
        prob_local_anota_ft,
        prob_local_anota_ht,
        prob_local_anota_2ht,
        prob_local_concede_ft,
        prob_local_concede_ht,
        prob_local_concede_2ht,
        prob_visitante_anota_ft,
        prob_visitante_anota_ht,
        prob_visitante_anota_2ht,
        prob_visitante_concede_ft,
        prob_visitante_concede_ht,
        prob_visitante_concede_2ht) = get_matches_both_team(match)

        (prob_over_05_ht,
        prob_over_15_ht,
        prob_over_05_ft,
        prob_over_15_ft,
        prob_over_25_ft,
        prob_over_35_ft,
        prob_over_05_mitad2,
        prob_aem_ft,
        prob_aem_ht,
        prob_aem_ht2,
        prob_win_home,
        prob_win_visit,
        prob_empate) = calcular_prob(total_matches,
                                    num_match_over_05_ht,
                                    num_match_over_15_ht,
                                    num_match_over_05_ft,
                                    num_match_over_15_ft,
                                    num_match_over_25_ft,
                                    num_match_over_35_ft,
                                    num_match_over_05_mitad2,
                                    num_match_aem_ft,
                                    num_match_aem_ht,
                                    num_match_aem_ht2,
                                    num_total_match_win_home,
                                    num_total_match_home,
                                    num_total_match_lose_visit,
                                    num_total_match_visit,
                                    num_total_match_win_visit,
                                    num_total_match_lose_home,
                                    num_total_match_empate_home,
                                    num_total_match_empate_visit)
        
        # ya tenemos todas las probabilidades del partido iterado. ahora hay que comparar esas prob con las de la estrategia
        print(match)
        if strategy_user.valor_ini_over_05_ht != None and cumple:
            if prob_over_05_ht >= strategy_user.valor_ini_over_05_ht and prob_over_05_ht <= strategy_user.valor_fin_over_05_ht:
                cumple = True
            else:
                cumple = False
            print('over 05 ht {}'.format(cumple))
        if strategy_user.valor_ini_over_15_ht != None and cumple:
            if prob_over_15_ht >= strategy_user.valor_ini_over_15_ht and prob_over_15_ht <= strategy_user.valor_fin_over_15_ht:
                cumple = True
            else:
                cumple = False
            print(cumple)
        if strategy_user.valor_ini_over_05_ft != None and cumple:
            if prob_over_05_ft >= strategy_user.valor_ini_over_05_ft and prob_over_05_ft <= strategy_user.valor_fin_over_05_ft:
                cumple = True
            else:
                cumple = False
            print(cumple)
        if strategy_user.valor_ini_over_15_ft != None and cumple:
            if prob_over_15_ft >= strategy_user.valor_ini_over_15_ft and prob_over_15_ft <= strategy_user.valor_fin_over_15_ft:
                cumple = True
            else:
                cumple = False
            print(cumple)
        if strategy_user.valor_ini_over_25_ft != None and cumple:
            if prob_over_25_ft >= strategy_user.valor_ini_over_25_ft and prob_over_25_ft <= strategy_user.valor_fin_over_25_ft:
                cumple = True
            else:
                cumple = False
            print(cumple)
        if strategy_user.valor_ini_aem != None and cumple:
            if prob_aem_ft >= strategy_user.valor_ini_aem and prob_aem_ft <= strategy_user.valor_fin_aem:
                cumple = True
            else:
                cumple = False
            print(cumple)
        if strategy_user.valor_ini_local_favorito != None and cumple:
            if prob_win_home > prob_win_visit:
                if prob_win_home >= strategy_user.valor_ini_local_favorito and prob_win_home <= strategy_user.valor_fin_local_favorito:
                    cumple = True
                else:
                    cumple = False
            else:
                cumple = False
            print(cumple)     
        if strategy_user.valor_ini_visitante_favorito != None and cumple:
            if prob_win_visit > prob_win_home:
                if prob_win_visit >= strategy_user.valor_ini_visitante_favorito and prob_win_visit <= strategy_user.valor_fin_visitante_favorito:
                    cumple = True
                else:
                    cumple = False
            else:
                cumple = False
            print(cumple)
        if strategy_user.valor_ini_local_anota_ft != None and cumple:
            if prob_local_anota_ft >= strategy_user.valor_ini_local_anota_ft and prob_local_anota_ft <= strategy_user.valor_fin_local_anota_ft:
                cumple = True
            else:
                cumple = False
            print(cumple)
        if strategy_user.valor_ini_local_anota_mitad_1 != None and cumple:
            if prob_local_anota_ht >= strategy_user.valor_ini_local_anota_mitad_1 and prob_local_anota_ht <= strategy_user.valor_fin_local_anota_mitad_1:
                cumple = True
            else:
                cumple = False
            print(cumple)
        if strategy_user.valor_ini_local_anota_mitad_2 != None and cumple:
            if prob_local_anota_2ht >= strategy_user.valor_ini_local_anota_mitad_2 and prob_local_anota_2ht <= strategy_user.valor_fin_local_anota_mitad_2:
                cumple = True
            else:
                cumple = False
            print(cumple)
        if strategy_user.valor_ini_visitante_anota_ft != None and cumple:
            if prob_visitante_anota_ft >= strategy_user.valor_ini_visitante_anota_ft and prob_visitante_anota_ft <= strategy_user.valor_fin_visitante_anota_ft:
                cumple = True
            else:
                cumple = False
            print(cumple)
        if strategy_user.valor_ini_visitante_anota_mitad_1 != None and cumple:
            if prob_visitante_anota_ht >= strategy_user.valor_ini_visitante_anota_mitad_1 and prob_visitante_anota_ht <= strategy_user.valor_fin_visitante_anota_mitad_1:
                cumple = True
            else:
                cumple = False
            print(cumple)

        if strategy_user.valor_ini_visitante_anota_mitad_2 != None and cumple:
            if prob_visitante_anota_2ht >= strategy_user.valor_ini_visitante_anota_mitad_2 and prob_visitante_anota_2ht <= strategy_user.valor_fin_visitante_anota_mitad_2:
                cumple = True
            else:
                cumple = False
            print(cumple)
        # toca ahora concede local y despues visitante
        if strategy_user.valor_ini_local_concede_ft != None and cumple:
            if prob_local_concede_ft >= strategy_user.valor_ini_local_concede_ft and prob_local_concede_ft <= strategy_user.valor_fin_concede_anota_ft:
                cumple = True
            else:
                cumple = False
            print(cumple)
        if strategy_user.valor_ini_local_concede_mitad_1 != None and cumple:
            if prob_local_concede_ht >= strategy_user.valor_ini_local_concede_mitad_1 and prob_local_concede_ht <= strategy_user.valor_fin_local_concede_mitad_1:
                cumple = True
            else:
                cumple = False
            print(cumple)
        if strategy_user.valor_ini_local_concede_mitad_2 != None and cumple:
            if prob_local_concede_2ht >= strategy_user.valor_ini_local_concede_mitad_2 and prob_local_concede_2ht <= strategy_user.valor_fin_local_concede_mitad_2:
                cumple = True
            else:
                cumple = False
            print(cumple)
        if strategy_user.valor_ini_visitante_concede_ft != None and cumple:
            if prob_visitante_concede_ft >= strategy_user.valor_ini_visitante_concede_ft and prob_visitante_concede_ft <= strategy_user.valor_fin_visitante_concede_ft:
                cumple = True
            else:
                cumple = False
            print(cumple)
        if strategy_user.valor_ini_visitante_concede_mitad_1 != None and cumple:
            if prob_visitante_concede_ht >= strategy_user.valor_ini_visitante_concede_mitad_1 and prob_visitante_concede_ht <= strategy_user.valor_fin_visitante_concede_mitad_1:
                cumple = True
            else:
                cumple = False
            print(cumple)

        if strategy_user.valor_ini_visitante_concede_mitad_2 != None and cumple:
            if prob_visitante_concede_2ht >= strategy_user.valor_ini_visitante_concede_mitad_2 and prob_visitante_concede_2ht <= strategy_user.valor_fin_visitante_concede_mitad_2:
                cumple = True
            else:
                cumple = False
            print(cumple)
        

        print('cumple final: {}'.format(cumple))

        if cumple == True:
            matches_strategy.append(match)
    
    return matches_strategy

        # --------------------------- Create your views here ------------------------------

class NextMatchesListView(ListView):
    model = Match
    template_name = 'forecasts/matches_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Próximos partidos de '

        league_id = get_object_or_404(League, id=self.kwargs['pk'])
        unplayed_matches = Match.objects.filter(league=league_id,gol_home_ht=None)  # aqui obtengo los que no se han jugado aun
        matches = get_next_matches_league(unplayed_matches)
        context['match_list'] = matches
        
        return context




class MatchDetailView(DetailView):
    model = Match
    template_name = 'forecasts/match_detail.html'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Pronósticos para     '

        # lógica para calcular las probabilidades de los diferentes mercados
        # ------------------------------------ over ht y ft ----------------------------------------
        
        (total_matches,
        num_match_over_05_ht,
        num_match_over_15_ht, 
        num_match_over_05_ft, 
        num_match_over_15_ft, 
        num_match_over_25_ft, 
        num_match_over_35_ft, 
        num_match_over_05_mitad2, 
        num_match_aem_ft, 
        num_match_aem_ht, 
        num_match_aem_ht2,
        num_total_match_win_home,
        num_total_match_lose_visit,
        num_total_match_win_visit,
        num_total_match_lose_home,
        num_total_match_empate_home,
        num_total_match_empate_visit,
        num_total_match_home,
        num_total_match_visit,
        prob_local_anota_ft,
        prob_local_anota_ht,
        prob_local_anota_2ht,
        prob_local_concede_ft,
        prob_local_concede_ht,
        prob_local_concede_2ht,
        prob_visitante_anota_ft,
        prob_visitante_anota_ht,
        prob_visitante_anota_2ht,
        prob_visitante_concede_ft,
        prob_visitante_concede_ht,
        prob_visitante_concede_2ht) = get_matches_both_team(self.get_object())

        (prob_over_05_ht,
        prob_over_15_ht,
        prob_over_05_ft,
        prob_over_15_ft,
        prob_over_25_ft,
        prob_over_35_ft,
        prob_over_05_mitad2,
        prob_aem_ft,
        prob_aem_ht,
        prob_aem_ht2,
        prob_win_home,
        prob_win_visit,
        prob_empate) = calcular_prob(total_matches,
                                    num_match_over_05_ht,
                                    num_match_over_15_ht,
                                    num_match_over_05_ft,
                                    num_match_over_15_ft,
                                    num_match_over_25_ft,
                                    num_match_over_35_ft,
                                    num_match_over_05_mitad2,
                                    num_match_aem_ft,
                                    num_match_aem_ht,
                                    num_match_aem_ht2,
                                    num_total_match_win_home,
                                    num_total_match_home,
                                    num_total_match_lose_visit,
                                    num_total_match_visit,
                                    num_total_match_win_visit,
                                    num_total_match_lose_home,
                                    num_total_match_empate_home,
                                    num_total_match_empate_visit)
            
            
        context['prob_win_home'] = round(prob_win_home,2)
        if prob_win_home != 0:
            context['cuota_win_home'] = np.round((1/prob_win_home)*100,2)
        else:
            context['cuota_win_home'] = 0
        context['prob_win_visit'] = round(prob_win_visit,2)
        if prob_win_visit != 0:
            context['cuota_win_visit'] = np.round((1/prob_win_visit)*100,2)
        else:
            context['cuota_win_visit'] = 0
        context['prob_empate'] = round(prob_empate,2)
        if prob_empate != 0:
            context['cuota_empate'] = np.round((1/prob_empate)*100,2)
        else:
            context['cuota_empate'] = 0        

        context['prob_over_05_ht'] = round(prob_over_05_ht,2)
        if prob_over_05_ht != 0:
            context['cuota_over_05_ht'] = np.round((1/prob_over_05_ht)*100,2)
        else:
            context['cuota_over_05_ht'] = 0
        context['prob_under_05_ht'] = round(100-prob_over_05_ht,2)
        if prob_over_05_ht != 100:
            context['cuota_under_05_ht'] = np.round((1/(100 - prob_over_05_ht))*100,2)
        else:
            context['cuota_under_05_ht'] = 0

        context['prob_over_15_ht'] = round(prob_over_15_ht,2)
        if prob_over_15_ht != 0:
            context['cuota_over_15_ht'] = np.round((1/prob_over_15_ht)*100,2)
        else:
            context['cuota_over_15_ht'] = 0
        context['prob_under_15_ht'] = round(100 - prob_over_15_ht,2)
        if prob_over_15_ht != 100:
            context['cuota_under_15_ht'] = np.round((1/(100 - prob_over_15_ht))*100,2)
        else:
            context['cuota_under_15_ht'] = 0

        context['prob_over_05_ft'] = round(prob_over_05_ft,2)
        if prob_over_05_ft != 0:
            context['cuota_over_05_ft'] = np.round((1/prob_over_05_ft)*100,2)
        else:
            context['cuota_over_05_ft'] = 0
        context['prob_under_05_ft'] = round(100-prob_over_05_ft,2)
        if prob_over_05_ft != 100:
            context['cuota_under_05_ft'] = np.round((1/(100 - prob_over_05_ft))*100,2)
        else:
            context['cuota_under_05_ft'] = 0

        context['prob_over_15_ft'] = round(prob_over_15_ft,2)
        if prob_over_15_ft != 0:
            context['cuota_over_15_ft'] = np.round((1/prob_over_15_ft)*100,2)
        else:
            context['cuota_over_15_ft'] = 0
        context['prob_under_15_ft'] = round(100 - prob_over_15_ft,2)
        if prob_over_15_ft != 100:
            context['cuota_under_15_ft'] = np.round((1/(100 - prob_over_15_ft))*100,2)
        else:
            context['cuota_under_15_ft'] = 0

        context['prob_over_25_ft'] = round(prob_over_25_ft,2)
        if prob_over_25_ft != 0:
            context['cuota_over_25_ft'] = np.round((1/prob_over_25_ft)*100,2)
        else:
            context['cuota_over_25_ft'] = 0
        context['prob_under_25_ft'] = round(100 - prob_over_25_ft,2)
        if prob_over_25_ft != 100:
            context['cuota_under_25_ft'] = np.round((1/(100 - prob_over_25_ft))*100,2)
        else:
            context['cuota_under_25_ft'] = 0

        context['prob_over_35_ft'] = round(prob_over_35_ft,2)
        if prob_over_35_ft != 0:
            context['cuota_over_35_ft'] = np.round((1/prob_over_35_ft)*100,2)
        else:
            context['cuota_over_35_ft'] = 0
        context['prob_under_35_ft'] = round(100 - prob_over_35_ft,2)
        if prob_over_35_ft != 100:
            context['cuota_under_35_ft'] = np.round((1/(100 - prob_over_35_ft))*100,2)
        else:
            context['cuota_under_35_ft'] = 0

        context['prob_over_05_mitad2'] = round(prob_over_05_mitad2,2)
        if prob_over_05_mitad2 != 0:
            context['cuota_over_05_mitad2'] = np.round((1/prob_over_05_mitad2)*100,2)
        else:
            context['cuota_over_05_mitad2'] = 0
        context['prob_under_05_mitad2'] = round(100 - prob_over_05_mitad2,2)
        if prob_over_05_mitad2 != 100:
            context['cuota_under_05_mitad2'] = np.round((1/(100 - prob_over_05_mitad2))*100,2)
        else:
            context['cuota_under_05_mitad2'] = 0

        context['prob_aem_ft'] = round(prob_aem_ft,2)
        if prob_aem_ft != 0:
            context['cuota_aem_ft'] = np.round((1/prob_aem_ft)*100,2)
        else:
            context['cuota_aem_ft'] = 0
        context['prob_aem_ft_no'] = round(100 - prob_aem_ft,2)
        if prob_aem_ft != 100:
            context['cuota_aem_ft_no'] = np.round((1/(100 - prob_aem_ft))*100,2)
        else:
            context['cuota_aem_ft_no'] = 0

        context['prob_aem_ht'] = round(prob_aem_ht,2)
        if prob_aem_ht != 0:
            context['cuota_aem_ht'] = np.round((1/prob_aem_ht)*100,2)
        else:
            context['cuota_aem_ht'] = 0
        context['prob_aem_ht_no'] = round(100 - prob_aem_ht,2)
        if prob_aem_ht != 100:
            context['cuota_aem_ht_no'] = np.round((1/(100 - prob_aem_ht))*100,2)
        else:
            context['cuota_aem_ht_no'] = 0

        context['prob_aem_ht2'] = round(prob_aem_ht2,2)
        if prob_aem_ht2 != 0:
            context['cuota_aem_ht2'] = np.round((1/prob_aem_ht2)*100,2)
        else:
            context['cuota_aem_ht2'] = 0
        context['prob_aem_h2t_no'] = round(100 - prob_aem_ht2,2)
        if prob_aem_ht2 != 100:
            context['cuota_aem_ht2_no'] = np.round((1/(100 - prob_aem_ht2))*100,2)
        else:
            context['cuota_aem_ht2_no'] = 0

        return context

def updateLive(request, pk):
    json_response = {'created': False}
    home_gol = request.GET.get('home_gol_ht', None)
    
    visit_gol = request.GET.get('visit_gol_ht', None)
    
    if home_gol != '' and visit_gol != '':
        # vamos a recuperar el partido
        goles_descanso = int(home_gol) + int(visit_gol)
        match = get_object_or_404(Match, pk=pk)
        prob_un_gol_mas, prob_dos_goles_mas, prob_tres_goles_mas = get_prob_goles_2ht_live(goles_descanso,match)
        if prob_un_gol_mas != 0:
            cuota_un_gol_mas = np.round((1/prob_un_gol_mas)*100,2)
        else:
            cuota_un_gol_mas = 0
        if prob_dos_goles_mas != 0:
            cuota_dos_goles_mas = np.round((1/prob_dos_goles_mas)*100,2)
        else:
            cuota_dos_goles_mas = 0
        if prob_tres_goles_mas != 0:
            cuota_tres_goles_mas = np.round((1/prob_tres_goles_mas)*100,2)
        else:
            cuota_tres_goles_mas = 0

        
        json_response['prob_un_gol_mas'] = prob_un_gol_mas
        json_response['cuota_un_gol_mas'] = cuota_un_gol_mas
        json_response['prob_dos_goles_mas'] = prob_dos_goles_mas
        json_response['cuota_dos_goles_mas'] = cuota_dos_goles_mas
        json_response['prob_tres_goles_mas'] = prob_tres_goles_mas
        json_response['cuota_tres_goles_mas'] = cuota_tres_goles_mas
        json_response['created'] = True
        
    else:
        raise Http404('Introduce el resultado al descanso')

    return JsonResponse(json_response)
    

def MatchesbyleaguesDate(request):
    title = 'Listado personalizado de partidos'
    
    if request.method == 'POST':
        form = MatchesForm(user=request.user, data=request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            leagues_select = form.cleaned_data['leagues']
            strategy = form.cleaned_data['strategies']
            matches = Match.objects.filter(
                date__range=(start_date, end_date),
                league__id__in=leagues_select,
                gol_home_ht=None)
            
            matches_strategy = get_matches_strategy(matches,strategy)
            
            return render(request, 'forecasts/matches_leagues_date_list.html', {
                'title': title,
                'form': form,
                'matches': matches_strategy
                })
    else:
        form = MatchesForm(user=request.user)
    return render(request, 'forecasts/matches_leagues_date_list.html', {
            'title': title,
            'form': form})


# vista para crear estrategias siempre que el usuario esté logueado
class StrategyCreateView(LoginRequiredMixin, CreateView):
    model = Strategy
    form_class = StrategyForm
    template_name = 'forecasts/strategy_form.html'
    success_url = reverse_lazy('strategies-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Estrategia'
        return context
    
    def form_valid(self, form):
        
        # Asociamos la estrategia al usuario logueado
        form.instance.user = self.request.user
        # Llamamos a la función original para guardar la estrategia
        response = super().form_valid(form)

        # Agregar mensaje de éxito
        messages.success(self.request, 'Estrategia creada exitosamente.')

        return response

# Vista para listar las estrategias de un usuario logueado
class StrategiesListView(ListView):
    model = Strategy
    #template_name = 'patients/patients_professional_list.html'
    template_name = 'forecasts/strategies_list.html'

    def get_queryset(self):
        return Strategy.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Mis Estrategias' 
        return context
    
    
class StrategyUpdateView(UpdateView):
    model = Strategy
    form_class = StrategyForm
    template_name = 'forecasts/strategy_form.html'
    success_url = reverse_lazy('strategies-list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Estrategia'
        return context

# vista para eliminar una estrategia
class StrategyDeleteView(DeleteView):
    model = Strategy
    template_name = 'forecasts/strategy_confirm_delete.html'
    success_url = reverse_lazy('strategies-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar estrategia'
        return context


