from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from bs4 import BeautifulSoup
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



def scraper(request):
    title = 'Scraper'
   
    leagues = League.objects.all()

    url = "https://www.resultados-futbol.com/"
    urls_match = []
    for league in leagues:
        url_league = '{}{}'.format(url,league.slug)
        req = requests.get(url_league, headers = headers).text
        soup = BeautifulSoup(req, 'html.parser')
        td_a_match = soup.find_all('td', {'class': 'rstd'})
        
        for td in td_a_match:
            a = td.find('a', {'class': 'url'})
            if a != None:
                #urls_match.append(a['href'].strip())
                req_match = requests.get('{}{}'.format(url,a['href'].strip()), headers = headers).text
                soup_match = BeautifulSoup(req,'html.parser')
                
                #print('{}{}'.format(url,a['href'].strip()))
            #url_match = a['href'].strip()
            #print('{}{}'.format(url,url_match))


        #req = requests.get(url)

    return render(request, 'feeder/scraper.html', {
        'title': title,
        
    })