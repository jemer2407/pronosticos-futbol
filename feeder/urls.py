from django.urls import path
from . import views


urlpatterns = [
    path('contry/', views.ContriesListView.as_view(), name="contry-list"),
    path('contry/create', views.ContryCreateView.as_view(), name="contry-create"),
    path('league/', views.LeaguesListView.as_view(), name="league-list"),
    path('league/contry/<int:pk>', views.LeaguesByContryListView.as_view(), name="league-contry-list"),
    path('league/create', views.LeagueCreateView.as_view(), name="league-create"),
    path('team/league/<int:pk>', views.TeamByLeagueListView.as_view(), name="team-league-list"),
    path('team/create', views.TeamCreateView.as_view(), name="team-create"),
    
]