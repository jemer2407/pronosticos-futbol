from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse, reverse_lazy
from forecasts.models import Contry, League, Team, Match
from feeder.forms import ContryForm, LeagueForm, TeamForm

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
        self.legue_id = get_object_or_404(League, id=self.kwargs['pk'])
        return Team.objects.filter(league=self.legue_id)

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


# crear la vista para crear los equipos y los partidos de todas las jornadas haciendo web scraping