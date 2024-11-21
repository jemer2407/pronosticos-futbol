from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Match

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



        return context