from django import forms
from django_flatpickr.widgets import DatePickerInput, TimePickerInput, DateTimePickerInput
from forecasts.models import League, Strategy


class MatchesForm(forms.Form):
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['strategies'].choices = Strategy.objects.filter(user=user).values_list('id', 'name')

    leagues = forms.MultipleChoiceField(choices=League.objects.all().values_list('id','name'),
                            widget=forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'leagues'}))
    start_date = forms.DateField(required=True,
                            widget=DatePickerInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'start_date'}))
    end_date = forms.DateField(required=True,
                               widget=DatePickerInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'end_date'}))
    strategies = forms.ChoiceField(choices=[],
                                widget=forms.Select(attrs={'class': 'form-control', 'id': 'strategy'}))
    

class StrategyForm(forms.ModelForm):
    class Meta:

        model = Strategy
        fields = ['name','valor_ini_over_05_ht','valor_fin_over_05_ht',
            'valor_ini_over_15_ht', 'valor_fin_over_15_ht',
            'valor_ini_over_05_ft','valor_fin_over_05_ft',
            'valor_ini_over_15_ft','valor_fin_over_15_ft',
            'valor_ini_over_25_ft','valor_fin_over_25_ft',
            'valor_ini_aem','valor_fin_aem',
            'valor_ini_local_anota_ft','valor_fin_local_anota_ft',
            'valor_ini_local_anota_mitad_1','valor_fin_local_anota_mitad_1',
            'valor_ini_local_anota_mitad_2','valor_fin_local_anota_mitad_2',
            'valor_ini_visitante_anota_ft','valor_fin_visitante_anota_ft',
            'valor_ini_visitante_anota_mitad_1','valor_fin_visitante_anota_mitad_1',
            'valor_ini_visitante_anota_mitad_2','valor_fin_visitante_anota_mitad_2',
            'valor_ini_local_concede_ft','valor_fin_local_concede_ft',
            'valor_ini_local_concede_mitad_1','valor_fin_local_concede_mitad_1',
            'valor_ini_local_concede_mitad_2','valor_fin_local_concede_mitad_2',
            'valor_ini_visitante_concede_ft','valor_fin_visitante_concede_ft',
            'valor_ini_visitante_concede_mitad_1','valor_fin_visitante_concede_mitad_1',
            'valor_ini_visitante_concede_mitad_2','valor_fin_visitante_concede_mitad_2',
            'valor_ini_local_favorito','valor_fin_local_favorito',
            'valor_ini_visitante_favorito','valor_fin_visitante_favorito']
                
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Introduce un nombre para la estrategia'}),
            
            'valor_ini_over_05_ht': forms.NumberInput(attrs={'class':'form-control',
                                                   'min':'0',
                                                   'max': '100'}),
            'valor_fin_over_05_ht': forms.NumberInput(attrs={'class':'form-control',
                                                   'min':'0',
                                                   'max': '100'}),
            'valor_ini_over_15_ht': forms.NumberInput(attrs={'class':'form-control',
                                                   'min':'0',
                                                   'max': '100'}),
            'valor_fin_over_15_ht': forms.NumberInput(attrs={'class':'form-control',
                                                   'min':'0',
                                                   'max': '100'}),
            'valor_ini_over_05_ft': forms.NumberInput(attrs={'class':'form-control',
                                                   'min':'0',
                                                   'max': '100'}),
            'valor_fin_over_05_ft': forms.NumberInput(attrs={'class':'form-control',
                                                   'min':'0',
                                                   'max': '100'}),
            'valor_ini_over_15_ft': forms.NumberInput(attrs={'class':'form-control',
                                                   'min':'0',
                                                   'max': '100'}),
            'valor_fin_over_15_ft': forms.NumberInput(attrs={'class':'form-control',
                                                   'min':'0',
                                                   'max': '100'}),
            'valor_ini_over_25_ft': forms.NumberInput(attrs={'class':'form-control',
                                                   'min':'0',
                                                   'max': '100'}),
            'valor_fin_over_25_ft': forms.NumberInput(attrs={'class':'form-control',
                                                   'min':'0',
                                                   'max': '100'}),
            'valor_ini_aem': forms.NumberInput(attrs={'class':'form-control',
                                                   'min':'0',
                                                   'max': '100'}),
            'valor_fin_aem': forms.NumberInput(attrs={'class':'form-control',
                                                   'min':'0',
                                                   'max': '100'}),
            'valor_ini_local_anota_ft': forms.NumberInput(attrs={'class':'form-control',
                                                   'min':'0',
                                                   'max': '100'}),
            'valor_fin_local_anota_ft': forms.NumberInput(attrs={'class':'form-control',
                                                   'min':'0',
                                                   'max': '100'}),
            'valor_ini_local_anota_mitad_1': forms.NumberInput(attrs={'class':'form-control',
                                                   'min':'0',
                                                   'max': '100'}),
            'valor_fin_local_anota_mitad_1': forms.NumberInput(attrs={'class':'form-control',
                                                   'min':'0',
                                                   'max': '100'}),
            'valor_ini_local_anota_mitad_2': forms.NumberInput(attrs={'class':'form-control',
                                                   'min':'0',
                                                   'max': '100'}),
            'valor_fin_local_anota_mitad_2': forms.NumberInput(attrs={'class':'form-control',
                                                   'min':'0',
                                                   'max': '100'}),
            'valor_ini_visitante_anota_ft': forms.NumberInput(attrs={'class':'form-control',
                                                   'min':'0',
                                                   'max': '100'}),
            'valor_fin_visitante_anota_ft': forms.NumberInput(attrs={'class':'form-control',
                                                   'min':'0',
                                                   'max': '100'}),
            'valor_ini_visitante_anota_mitad_1': forms.NumberInput(attrs={'class':'form-control',
                                                   'min':'0',
                                                   'max': '100'}),
            'valor_fin_visitante_anota_mitad_1': forms.NumberInput(attrs={'class':'form-control',
                                                   'min':'0',
                                                   'max': '100'}),
            'valor_ini_visitante_anota_mitad_2': forms.NumberInput(attrs={'class':'form-control',
                                                   'min':'0',
                                                   'max': '100'}),
            'valor_fin_visitante_anota_mitad_2': forms.NumberInput(attrs={'class':'form-control',
                                                   'min':'0',
                                                   'max': '100'}),
            'valor_ini_local_concede_ft': forms.NumberInput(attrs={'class':'form-control',
                                                   'min':'0',
                                                   'max': '100'}),
            'valor_fin_local_concede_ft': forms.NumberInput(attrs={'class':'form-control',
                                                   'min':'0',
                                                   'max': '100'}),
            'valor_ini_local_concede_mitad_1': forms.NumberInput(attrs={'class':'form-control',
                                                   'min':'0',
                                                   'max': '100'}),
            'valor_fin_local_concede_mitad_1': forms.NumberInput(attrs={'class':'form-control',
                                                   'min':'0',
                                                   'max': '100'}),
            'valor_ini_local_concede_mitad_2': forms.NumberInput(attrs={'class':'form-control',
                                                   'min':'0',
                                                   'max': '100'}),
            'valor_fin_local_concede_mitad_2': forms.NumberInput(attrs={'class':'form-control',
                                                   'min':'0',
                                                   'max': '100'}),
            'valor_ini_visitante_concede_ft': forms.NumberInput(attrs={'class':'form-control',
                                                   'min':'0',
                                                   'max': '100'}),
            'valor_fin_visitante_concede_ft': forms.NumberInput(attrs={'class':'form-control',
                                                   'min':'0',
                                                   'max': '100'}),
            'valor_ini_visitante_concede_mitad_1': forms.NumberInput(attrs={'class':'form-control',
                                                   'min':'0',
                                                   'max': '100'}),
            'valor_fin_visitante_concede_mitad_1': forms.NumberInput(attrs={'class':'form-control',
                                                   'min':'0',
                                                   'max': '100'}),
            'valor_ini_visitante_concede_mitad_2': forms.NumberInput(attrs={'class':'form-control',
                                                   'min':'0',
                                                   'max': '100'}),
            'valor_fin_visitante_concede_mitad_2': forms.NumberInput(attrs={'class':'form-control',
                                                   'min':'0',
                                                   'max': '100'}),
            'valor_ini_local_favorito': forms.NumberInput(attrs={'class':'form-control',
                                                   'min':'0',
                                                   'max': '100'}),
            'valor_fin_local_favorito': forms.NumberInput(attrs={'class':'form-control',
                                                   'min':'0',
                                                   'max': '100'}),
            'valor_ini_visitante_favorito': forms.NumberInput(attrs={'class':'form-control',
                                                   'min':'0',
                                                   'max': '100'}),
            'valor_fin_visitante_favorito': forms.NumberInput(attrs={'class':'form-control',
                                                   'min':'0',
                                                   'max': '100'}),
            
            
        }
        labels = {
            'name' : '',            
            'valor_ini_over_05_ht': 'Over 0.5 HT desde (%)',
            'valor_fin_over_05_ht': 'Over 0.5 HT hasta (%)',
            'valor_ini_over_15_ht': 'Over 1.5 HT desde (%)',
            'valor_fin_over_15_ht': 'Over 1.5 HT hasta (%)',
            'valor_ini_over_05_ft': 'Over 0.5 FT desde (%)',
            'valor_fin_over_05_ft': 'Over 0.5 FT hasta (%)',
            'valor_ini_over_15_ft': 'Over 1.5 FT desde (%)',
            'valor_fin_over_15_ft': 'Over 1.5 FT hasta (%)',
            'valor_ini_over_25_ft': 'Over 2.5 FT desde (%)',
            'valor_fin_over_25_ft': 'Over 2.5 FT hasta (%)',
            'valor_ini_aem': 'AEM desde (%)',
            'valor_fin_aem': 'AEM hasta (%)',
            'valor_ini_local_anota_ft': 'Local anota FT desde (%)',
            'valor_fin_local_anota_ft': 'Local anota FT hasta (%)',
            'valor_ini_local_anota_mitad_1': 'Local anota 1ª mitad desde (%)',
            'valor_fin_local_anota_mitad_1': 'Local anota 1ª mitad (%)',
            'valor_ini_local_anota_mitad_2': 'Local anota 2ª mitad desde (%)',
            'valor_fin_local_anota_mitad_2': 'Local anota 2ª mitad hasta (%)',
            'valor_ini_visitante_anota_ft': 'Visitante anota 2ª mitad desde (%)',
            'valor_fin_visitante_anota_ft': 'Visitante anota 2ª mitad hasta (%)',
            'valor_ini_visitante_anota_mitad_1': 'Visitante anota 1ª mitad desde (%)',
            'valor_fin_visitante_anota_mitad_1': 'Visitante anota 1ª mitad hasta (%)',
            'valor_ini_visitante_anota_mitad_2': 'Visitante anota 2ª mitad desde (%)',
            'valor_fin_visitante_anota_mitad_2': 'Visitante anota 2ª mitad hasta (%)',
            'valor_ini_local_concede_ft': 'Local concede FT desde (%)',
            'valor_fin_local_concede_ft': 'Local concede FT hasta (%)',
            'valor_ini_local_concede_mitad_1': 'Local concede 1ª mitad desde (%)',
            'valor_fin_local_concede_mitad_1': 'Local concede 1ª mitad hasta (%)',
            'valor_ini_local_concede_mitad_2': 'Local concede 2ª mitad desde (%)',
            'valor_fin_local_concede_mitad_2': 'Local concede 2ª mitad hasta (%)',
            'valor_ini_visitante_concede_ft': 'Visitante concede FT desde (%)',
            'valor_fin_visitante_concede_ft': 'Visitante concede FT hasta (%)',
            'valor_ini_visitante_concede_mitad_1': 'Visitante concede 1ª mitad desde (%)',
            'valor_fin_visitante_concede_mitad_1': 'Visitante concede 1ª mitad hasta (%)',
            'valor_ini_visitante_concede_mitad_2': 'Visitante concede 2ª mitad desde (%)',
            'valor_fin_visitante_concede_mitad_2': 'Visitante concede 2ª mitad hasta (%)',
            'valor_ini_local_favorito': 'Local favorito desde (%)',
            'valor_fin_local_favorito': 'Local favorito hasta (%)',
            'valor_ini_visitante_favorito': 'Visitante favorito desde (%)',
            'valor_fin_visitante_favorito': 'Visitante favorito hasta (%)'            
        }
    def clean(self):
        cleaned_data = super().clean()

        # Validación de valores iniciales y finales
        for field_name in ['over_05_ht', 'over_15_ht', 'over_05_ft', 'over_15_ft', 'over_25_ft', 'aem', 'local_anota_ft', 'local_anota_mitad_1', 'local_anota_mitad_2', 'visitante_anota_ft', 'visitante_anota_mitad_1', 'visitante_anota_mitad_2', 'local_concede_ft', 'local_concede_mitad_1', 'local_concede_mitad_2', 'visitante_concede_ft', 'visitante_concede_mitad_1', 'visitante_concede_mitad_2', 'local_favorito', 'visitante_favorito']:
            valor_ini = cleaned_data.get(f'valor_ini_{field_name}')
            valor_fin = cleaned_data.get(f'valor_fin_{field_name}')

            if valor_ini and valor_fin and valor_ini > valor_fin:
                raise forms.ValidationError(f"El valor inicial de {field_name} debe ser menor o igual al valor final.")

        return cleaned_data
    

                           
    
