from django.urls import path
from . import views


urlpatterns = [
    path('<int:pk>/', views.NextMatchesListView.as_view(), name="next-matchs-list"),
    path('match/<int:pk>/', views.MatchDetailView.as_view(), name="match-detail"),
    path('match/live/<int:pk>/', views.updateLive, name="update-live"),
    path('matches/', views.MatchesbyleaguesDate, name="matches-leagues-date-list"),
    path('strategy/', views.StrategyCreateView.as_view(), name="strategy-create"),
    path('strategy/list/', views.StrategiesListView.as_view(), name="strategies-list"),
    path('strategy/update/<int:pk>/', views.StrategyUpdateView.as_view(), name='strategy-update'),
    path('strategy/delete/<int:pk>/', views.StrategyDeleteView.as_view(), name='strategy-delete')
]