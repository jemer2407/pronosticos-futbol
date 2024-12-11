#from django.contrib.auth.forms import UserCreationForm  # formulario generico de django para el registro de usuarios
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import redirect

from registration.models import Profile
from .forms import EmailForm, ProfileForm, UserCreationFormWithEmail

from django.views.generic import CreateView # Clase de la que vamos a heredar para crear una vista de Creación de un registro
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.generic.edit import UpdateView
import stripe
from django import forms



# Create your views here.
# Vista basada en clase para el registro de usuarios
class SignUpView(CreateView):
    #form_class = UserCreationForm   # Esta clase es el formulario que nos proporciona django por defecto para el registro de usuarios
    form_class = UserCreationFormWithEmail
    success_url = reverse_lazy('login') # redirigir a la pagina de login despues de registrarse
    template_name = 'registration/signup.html'  # template para el registro de usuario

    def get_success_url(self):
        return reverse_lazy('login') + '?register'
    
    def get_form(self, form_class=None):
        form = super(SignUpView, self).get_form()
        # Modificar en tiempo real el formulario
        form.fields['username'].widget = forms.TextInput(
            attrs={
            'class':'form-control mb-2', 
            'placeholder':'Nombre de usuario'
            })
        form.fields['email'].widget = forms.EmailInput(
            attrs={
                'class':'form-control mb-2', 
                'placeholder':'Email'
                })
        form.fields['password1'].widget = forms.PasswordInput(
            attrs={
                'class':'form-control mb-2', 
                'placeholder':'Contraseña'
                })
        form.fields['password2'].widget = forms.PasswordInput(
            attrs={
            'class':'form-control mb-2', 
            'placeholder':'Repita contraseña'
            })
        return form
    
@method_decorator(login_required, name='dispatch')
class ProfileUpdate(UpdateView):
    form_class = ProfileForm
    success_url = reverse_lazy('profile')
    template_name = 'registration/profile_form.html'

    def get_object(self):
        # recuperar el objeto que se va a editar
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile


@method_decorator(login_required, name='dispatch')
class EmailUpdate(UpdateView):
    form_class = EmailForm
    success_url = reverse_lazy('profile')
    template_name = 'registration/profile_email_form.html'

    def get_object(self):
        # recuperar el objeto que se va a editar
       
        return self.request.user
    
    def get_form(self, form_class = None):
        form = super(EmailUpdate, self).get_form()
        # Modificar en tiempo real el formulario
        form.fields['email'].widget = forms.EmailInput(
            attrs={
            'class':'form-control mb-2', 
            'placeholder':'Email'
            })
        return form
