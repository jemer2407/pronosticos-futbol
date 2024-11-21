from django.urls import path
from . import views

urlpatterns = [
    path('', views.NextMatchesListView.as_view(), name="next-matchs-list"),
    path('match/<int:pk>', views.MatchDetailView.as_view(), name="match-detail"),   
]