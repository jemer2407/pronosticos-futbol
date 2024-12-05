from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Subscriber

class SuscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = '__all__'
        widgets = {
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Email'})
            
        }
        labels = {
            'email':''
        }

class EmailMarketingForm(forms.Form):

    subject = forms.CharField(label='', required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Escribe el asunto'}
    ), max_length=100)
    message = forms.CharField(label='Mensaje', required=True, widget=SummernoteWidget(
        attrs={'class': 'form-control'}
    ), min_length=10, max_length=1000)