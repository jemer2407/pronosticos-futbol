from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from datetime import datetime
from django.conf import settings
from bs4 import BeautifulSoup
import os
import re
import unicodedata
import requests
from forecasts.models import Contry, League, Team, Match
from feeder.forms import ContryForm, LeagueForm, TeamForm


url = "https://www.resultados-futbol.com/"
headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
}

# función que devuelve una cadena de texto sin acentos, simbolos y carecteres especiales, conservando
# letras y espacios
def limpiar_texto(texto):
    
    # Normalizamos la cadena para descomponer los caracteres con diacríticos
    texto_normalizado = unicodedata.normalize('NFD', texto)
    # Eliminamos los caracteres que no sean letras, números o espacios
    texto_limpio = re.sub(r'[^a-zA-Z0-9\s.-]', '', texto_normalizado)
    return texto_limpio



# Create your views here.

class ContriesListView(ListView):
    model = Contry
    template_name = 'feeder/contries_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Paises'
        return context

class ContryCreateView(CreateView):
    model = Contry
    form_class = ContryForm
    template_name = 'feeder/contry_form.html'
    success_url = reverse_lazy('contry-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Pais'
        return context

class LeaguesListView(ListView):
    model = League
    template_name = 'feeder/leagues_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Ligas'
        return context

class LeaguesByContryListView(ListView):
    model = League
    template_name = 'feeder/leagues_list.html'

    def get_queryset(self):
        self.contry_id = get_object_or_404(Contry, id=self.kwargs['pk'])
        return League.objects.filter(contry=self.contry_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Ligas'
        return context


class LeagueCreateView(CreateView):
    model = League
    form_class = LeagueForm
    template_name = 'feeder/league_form.html'
    success_url = reverse_lazy('league-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nueva Liga'
        return context


class TeamByLeagueListView(ListView):
    model = Team
    template_name = 'feeder/teams_list.html'

    def get_queryset(self):
        self.league_id = get_object_or_404(League, id=self.kwargs['pk'])
        return Team.objects.filter(league=self.league_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Equipos'
        return context

class TeamCreateView(CreateView):
    model = Team
    form_class = TeamForm
    template_name = 'feeder/team_form.html'
    success_url = reverse_lazy('team-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Equipo'
        return context

class MatchesByTeamListView(ListView):
    model = Match
    template_name = 'forecasts/matches_list.html'

    def get_queryset(self):
        self.team_id = get_object_or_404(Team, id=self.kwargs['pk'])
        return Match.objects.filter((Q(home_team=self.team_id) | Q(visit_team=self.team_id)), Q(gol_home_ht=None))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Partidos'
        context['first_match'] = True
        return context


# vista para obtener los proximos partidos de todas las ligas, ordenarlas por fechas y mostrarlas en la home




# crear la vista para crear los equipos y los partidos de todas las jornadas haciendo web scraping



def scraper_resultados(request):
    title = 'Scraper'
   
    leagues = League.objects.all()

    #url = "https://www.resultados-futbol.com/"
    urls_match = []
    for league in leagues:
        print(league)
        url_league = '{}{}'.format(url,league.slug)
        req = requests.get(url_league, headers = headers).text
        soup = BeautifulSoup(req, 'html.parser')
        td_a_match = soup.find_all('td', {'class': 'rstd'})
        
        for td in td_a_match:
            a = td.find('a', {'class': 'url'})
            if a != None:
                #urls_match.append(a['href'].strip())
                req_match = requests.get('{}{}'.format(url,a['href'].strip()), headers = headers).text
                soup_match = BeautifulSoup(req_match,'html.parser')
                etiq_soccer_day = soup_match.find('div', {'class': 'jornada'}).find('a')

                if soup_match.find('span',{'class':"jor-status jor-finished"}):
                    
                    if soup_match.find('span',{'class':"jor-status jor-finished"}).text == 'FINALIZADO':
                        soccer_day = etiq_soccer_day.text[8:10]
                        etiq_teams = soup_match.find('div',{'class': 'performers'}).find_all('h2')
                        
                        home_team = etiq_teams[0].text
                        visit_team = etiq_teams[1].text
                        etiq_goles_ft = soup_match.find_all('span', {'class': 'claseR'})
                        home_gol_ft = etiq_goles_ft[0].text
                        visit_gol_ft = etiq_goles_ft[1].text
                        # ------- obtener gol marcado en el trascurso del partido ---------
                        etiq_goles = soup_match.find_all('td', {'class': 'mhr-marker'})
                        goles = []
                        for etiq in etiq_goles:
                            etiq_gol = etiq.find('div').text
                            goles.append([int(digito) for digito in etiq_gol if digito.isdigit()])
                        
                        

                        # ------- obtener minuto del gol marcado en el trascurso del partido ---------
                        etiq_min_gol = soup_match.find_all('td', {'class': 'mhr-min'})
                        
                        if etiq_min_gol != None:
                            minutos_goles = []
                            for etiq in etiq_min_gol:
                                if etiq.text != '':
                                    eliminar = "'"
                                    minutos_goles.append(int(etiq.text.replace(eliminar,"")))
                        
                        

                        # ------- calcular marcador en el descanso ---------
                        marcador_ht = [0,0]
                        for gol,min in zip(goles,minutos_goles):
                            
                            if min<=45:
                                if gol[0]==marcador_ht[0]:
                                    marcador_ht[1]+=1
                                else:
                                    marcador_ht[0]+=1
                        
                        #print(soccer_day)
                        

                        
                        home_team_format = limpiar_texto(home_team)
                        print(home_team)
                        print(home_team_format)
                        visit_team_format = limpiar_texto(visit_team)
                        print(visit_team)
                        print(visit_team_format)
                        obj_local = Team.objects.get(team=home_team_format)
                        obj_visit = Team.objects.get(team=visit_team_format)
                        
                        match_obj = Match.objects.get(home_team=obj_local.id,visit_team=obj_visit.id)
                        if match_obj.gol_home_ht == None:
                            match_obj.gol_home_ht = marcador_ht[0]
                            match_obj.gol_visit_ht = marcador_ht[1]
                            match_obj.gol_home_ft = home_gol_ft
                            match_obj.gol_visit_ft = visit_gol_ft
                            match_obj.save()
                        else:
                            print('{} - {} ya actualizado'.format(home_team_format, visit_team_format))
                    
                    
                
                #print('{}{}'.format(url,a['href'].strip()))
            #url_match = a['href'].strip()
            #print('{}{}'.format(url,url_match))


        #req = requests.get(url)

    return render(request, 'feeder/scraper_score.html', {
        'title': title,
        
    })



def scraper_create_teams(request):
    title = 'Crear Equipos de Ligas dadas de alta'
    leagues = League.objects.all()
    
    #url = "https://www.resultados-futbol.com/"
    
    for league in leagues:
        print(league.name)
        if not Team.objects.filter(league=league):
            url_league = '{}{}'.format(url,league.slug)
            req = requests.get(url_league, headers = headers).text
            soup = BeautifulSoup(req, 'html.parser')
            tds_team = soup.find_all('td', {'class': 'equipo'})
            for td_team in tds_team:
                team = td_team.find('a').text
                print(team)
                etiq_img = td_team.find('img')
                url_img = etiq_img['src']
                # descargar la imagen del equipo
                response_img = requests.get(url_img) # peticion a la url de la imagen
                if response_img.status_code == 200:
                    # guardamos la imagen
                    ruta_completa = os.path.join(settings.MEDIA_ROOT, 'team/', "{}_img.jpg".format(team))
                    with open(ruta_completa, "wb") as archivo:
                        archivo.write(response_img.content)
                        print(ruta_completa)
                        print("¡La imagen del escudo del Arsenal se ha descargado correctamente!")
                else:
                    print("Error al descargar la imagen. Código de estado:", response_img.status_code)
                print(url_img)
                
                # guardar datos en la tabla Team (team, league, image('team/nombre_archivo'))
                # creamos el objeto team
                team_format = limpiar_texto(team)
                team_obj = Team(team=team_format,league=league,image='team/{}_img.jpg'.format(team_format))
                team_obj.save()
                
    return render(request, 'feeder/scraper_create_league.html', {
        'title': title,
        
    })

def scraper_create_matches(request):

    title = 'Crear partidos de la liga'
    leagues = League.objects.all()

    for league in leagues:
        if not Match.objects.filter(league=league):
            j = 1           
            teams = Team.objects.filter(league=league)
            soccer_days = (len(teams)*2)-2 # numero de jornadas que hay en esa liga
            while j<=soccer_days:
                url_league = '{}{}/grupo1/jornada{}'.format(url,league.slug,j)
                scraper_data_match(url_league, league, j)
                j+=1

    return render(request, 'feeder/scraper_create_matches.html', {
            'title': title,
            
        })



def scraper_data_match(url_league, league, soccer_day):
    print(url_league)
    #url_jor_league = '{}{}'.format(url,url_league)
    req = requests.get(url_league, headers = headers).content.decode('utf-8')
    soup = BeautifulSoup(req, 'html.parser')
    home_gol_ft=None
    visit_gol_ft=None
    home_gol_ht=None
    visit_gol_ht=None
    etiq_table = soup.find('table', {'id': 'tabla1'})
    if etiq_table.find_all('a', {'class': 'url'}) or etiq_table.find_all('a', {'class': 'hour'}):
        etiq_aes_jugado = etiq_table.find_all('a', {'class': 'url'})   # todas las etiquetas a de partido jugado
        etiq_aes_no_jugado = etiq_table.find_all('a', {'class': 'hour'})   # todas las etiquetas a de partido NO jugado
    
        urls_matches = []
        for etiq_a_jugado in etiq_aes_jugado:   
            urls_matches.append(etiq_a_jugado['href'])  # guardamos en urls_matches las url de los partidos jugados
    
        for etiq_a_no_jugado in etiq_aes_no_jugado:
            urls_matches.append(etiq_a_no_jugado['href'])   # guardamos en urls_matches las url de los partidos no jugados

        for url_match in urls_matches:  # iteramos la lista urls_matches para ir entrando en la url del partido para sacar los datos necesarios
            url_completa_match = '{}{}'.format(url,url_match)
            req_match = requests.get(url_completa_match, headers = headers).content.decode('utf-8')
            soup_match = BeautifulSoup(req_match, 'html.parser')
            # equipo local
            
            etiq_div_team1 = soup_match.find('div', {'class': 'team equipo1'})
            try:
                etiq_a_local_team = etiq_div_team1.find('a')
                local_team = etiq_a_local_team.text
            except:
                local_team = etiq_div_team1.find('b').text
                
            # equipo visitante
            etiq_div_team2 = soup_match.find('div', {'class': 'team equipo2'})
            try:
                away_team = etiq_div_team2.find('a').text
            except:
                away_team = etiq_div_team2.find('b').text
            # fecha del partido    
            date_span = soup_match.find('span',{'class': 'jor-date'})['content']
            date_scraped = datetime.strptime(date_span, "%Y-%m-%dT%H:%M:%S%z")
            date = date_scraped.strftime("%Y-%m-%d")
            # resultado del partido
            
            etiq_div_resul = soup_match.find('div', {'class': 'resultado resultadoH'})
            
            if etiq_div_resul.find_all('span',{'class': 'claseR'}): # si hay un resultado en el marcador
                etiq_span_gol = etiq_div_resul.find_all('span',{'class': 'claseR'})
                home_gol_ft = etiq_span_gol[0].text
                visit_gol_ft = etiq_span_gol[1].text
                if home_gol_ft == 0 and visit_gol_ft == 0:
                    home_gol_ht = 0
                    visit_gol_ht = 0
                else:
                    if not home_gol_ft.isdigit():
                        home_gol_ht = None
                        home_gol_ft = None
                    
                    if not visit_gol_ft.isdigit():
                        visit_gol_ht = None
                        visit_gol_ft = None
                
                
        
                    # ------- obtener gol marcado en el trascurso del partido ---------
                    goles = []
                    if soup_match.find_all('td', {'class': 'mhr-marker'}):
                        etiq_goles = soup_match.find_all('td', {'class': 'mhr-marker'})
                        
                        for etiq in etiq_goles:
                            etiq_gol = etiq.find('div').text
                            goles.append([int(digito) for digito in etiq_gol if digito.isdigit()])
                
                

                        # ------- obtener minuto del gol marcado en el trascurso del partido ---------
                        etiq_min_gol = soup_match.find_all('td', {'class': 'mhr-min'})
                        
                        if etiq_min_gol != None:
                            minutos_goles = []
                            for etiq in etiq_min_gol:
                                if etiq.text != '':
                                    eliminar = "'"
                                    minutos_goles.append(int(etiq.text.replace(eliminar,"")))
                    
                    

                        # ------- calcular marcador en el descanso ---------

                        marcador_ht = [0,0]
                        for gol,min in zip(goles,minutos_goles):
                            
                            if min<=45:
                                if gol[0]==marcador_ht[0]:
                                    marcador_ht[1]+=1
                                else:
                                    marcador_ht[0]+=1

                
                        home_gol_ht=marcador_ht[0]
                        visit_gol_ht=marcador_ht[1]
        

            print(league)
            print('jornada {}'.format(soccer_day))
            print(date)
            print('{} {} ({}) - ({}) {} {}'.format(local_team,home_gol_ft,home_gol_ht,visit_gol_ht,visit_gol_ft,away_team))
        
            home_team_format = limpiar_texto(local_team)
            print(home_team_format)
            home_team = Team.objects.get(team=home_team_format)
            print(home_team)

            visit_team_format = limpiar_texto(away_team)
            print(visit_team_format)
            visit_team = Team.objects.get(team=visit_team_format)
            print(visit_team)

            match_obj = Match(league=league,
                            soccer_day=soccer_day,
                            home_team=home_team,
                            visit_team=visit_team,
                            date=date,
                            gol_home_ht=home_gol_ht,
                            gol_visit_ht=visit_gol_ht,
                            gol_home_ft=home_gol_ft,
                            gol_visit_ft=visit_gol_ft
                            )
            match_obj.save()
    else:
        #etiq_span_no_jugado = etiq_table.find_all('span', {'class': 'clase'})
        etiq_equipo_1 = etiq_table.find_all('td', {'class': 'equipo1'})
        etiq_equipo_2 = etiq_table.find_all('td', {'class': 'equipo2'})
        etiq_td_fecha = etiq_table.find_all('td', {'class': 'fecha'})

        for equipo1,equipo2,fecha in zip(etiq_equipo_1,etiq_equipo_2,etiq_td_fecha):
            # equipo local
            etiq_a_equipo1 = equipo1.find_all('a')
            local_team = etiq_a_equipo1[-1].text
            # equipo visitante
            etiq_a_equipo2 = equipo2.find_all('a')
            away_team = etiq_a_equipo2[-1].text
            # fecha del partido    
            date_match = fecha['data-date']
            date_scraped = datetime.strptime(date_match, "%a, %d %b %Y %H:%M:%S %z")
            date = date_scraped.strftime("%Y-%m-%d")

            home_team_format = limpiar_texto(local_team)
            print(home_team_format)
            home_team = Team.objects.get(team=home_team_format)
            print(home_team)

            visit_team_format = limpiar_texto(away_team)
            print(visit_team_format)
            visit_team = Team.objects.get(team=visit_team_format)
            print(visit_team)

            match_obj = Match(league=league,
                            soccer_day=soccer_day,
                            home_team=home_team,
                            visit_team=visit_team,
                            date=date,
                            gol_home_ht=home_gol_ht,
                            gol_visit_ht=visit_gol_ht,
                            gol_home_ft=home_gol_ft,
                            gol_visit_ft=visit_gol_ft
                            )
            match_obj.save()