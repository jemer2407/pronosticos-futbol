from django import forms
from forecasts.models import Contry, League, Team

class ContryForm(forms.ModelForm):
    
    class Meta:
        model = Contry
        fields = '__all__'
        
        
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Nombre'}),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control-file mt-3'})
        }
        
        labels = {
            'name':'', 
            'image':'Bandera del pais'
        }


class LeagueForm(forms.ModelForm):
    
    class Meta:
        model = League
        fields = '__all__'
        
        
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Nombre'}),
            'season': forms.Select(attrs={'class':'form-control'}),
            'contry': forms.Select(attrs={'class':'form-control'}),
        }
        
        labels = {
            'name':'', 
            'season':'Temporada',
            'contry': 'Pais'
        }


class TeamForm(forms.ModelForm):
    
    class Meta:
        model = Team
        fields = '__all__'
        
        
        widgets = {
            'team': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Nombre del equipo'}),
            'league': forms.Select(attrs={'class':'form-control'}),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control-file mt-3'})
        }
        
        labels = {
            'team':'', 
            'league':'Liga',
            'image': 'Escudo'
        }