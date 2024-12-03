from django import forms
from django_flatpickr.widgets import DatePickerInput, TimePickerInput, DateTimePickerInput
from forecasts.models import Match, League



class MatchesForm(forms.Form):
    leagues = forms.MultipleChoiceField(choices=League.objects.all().values_list('id','name'),
                            widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
                            required=False
                            )
    start_date = forms.DateField(required=True,
                            widget=DatePickerInput(attrs={'class': 'form-control', 'type': 'date'}))
    
    end_date = forms.DateField(required=True,
                            widget=DatePickerInput(attrs={'class': 'form-control', 'type': 'date'}))
    

    

                           
    
