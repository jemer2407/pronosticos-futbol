from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.conf import settings
from bs4 import BeautifulSoup
import os
import requests
from forecasts.models import Contry, League, Team, Match
from feeder.forms import ContryForm, LeagueForm, TeamForm

headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
}


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
        return context

# crear la vista para crear los equipos y los partidos de todas las jornadas haciendo web scraping



def scraper_resultados(request):
    title = 'Scraper'
   
    leagues = League.objects.all()

    url = "https://www.resultados-futbol.com/"
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
                    
                    print('{} {} ({})-({}) {} {}'.format(home_team,home_gol_ft, marcador_ht[0],marcador_ht[1],visit_gol_ft,visit_team))

                    
                    
                
                #print('{}{}'.format(url,a['href'].strip()))
            #url_match = a['href'].strip()
            #print('{}{}'.format(url,url_match))


        #req = requests.get(url)

    return render(request, 'feeder/scraper_score.html', {
        'title': title,
        
    })



def scraper_create_league(request):
    title = 'Crear nueva liga'
    leagues = League.objects.all()
    
    url = "https://www.resultados-futbol.com/"
    urls_match = []
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

    return render(request, 'feeder/scraper_create_league.html', {
        'title': title,
        
    })