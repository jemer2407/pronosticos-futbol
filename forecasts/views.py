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
        form = MatchesForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            leagues_select = form.cleaned_data['leagues']
            matches = Match.objects.filter(
                date__range=(start_date, end_date),
                league__id__in=leagues_select,
                gol_home_ht=None)
            return render(request, 'forecasts/matches_leagues_date_list.html', {
                'title': title,
                'form': form,
                'matches': matches})
    else:
        form = MatchesForm()
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