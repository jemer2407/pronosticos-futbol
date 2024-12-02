from django import forms
from forecasts.models import Match, League

class MatchesForm(forms.Form):
    leagues_obj = League.objects.all()
    leagues = {}
    for league in leagues_obj:
        leagues[league.id] = league.name
        

    print(leagues)
    league = forms.MultipleChoiceField(label='Ligas', required=True, widget=forms.SelectMultiple(
        choices=leagues,
        attrs={'class': 'form-control'}
    ))
    date = forms.DateField(label='Fecha', required=True, widget=forms.DateInput(
        attrs={'class': 'form-control', 'type': 'date', 'id':'id_date'}
    ))
    
    
