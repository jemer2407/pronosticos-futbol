
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.urls import reverse

from registration.models import Profile
from .forms import ContactForm
from django.core.mail import EmailMessage
from django.utils import timezone
from forecasts.models import Match, Contry, League, Strategy
from forecasts.views import get_next_matches_league

class HomeView(TemplateView):
    model = Match
    template_name = "core/home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Estratebet - Versión Beta'
        leagues = League.objects.all()
        context['leagues'] = leagues
        # proximos partidos de todas las ligas
        next_unplayed_matches = []
        for league in leagues:
            unplayed_matches = Match.objects.filter(league=league.id,gol_home_ht=None)  # aqui obtengo los que no se han jugado aun
            matches = get_next_matches_league(unplayed_matches)
            next_unplayed_matches.append(matches)
        
        context['next_matches_leagues_list'] = next_unplayed_matches
        if self.request.user.is_authenticated:
            context['user'] = self.request.user
            profile = Profile.objects.get(user=self.request.user)
            context['profile'] = profile
        
        return context

class AboutView(TemplateView):
    template_name = "core/about.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'title': 'Sobre nosotros'
        })
    
def contact(request):
    title = 'Contacto'
   
    contact_form = ContactForm()
    if request.method == 'POST':
        contact_form = ContactForm(data=request.POST)
        if contact_form.is_valid():
            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            content = request.POST.get('content', '')

            # Enviamos el correo y redireccionamos

            email = EmailMessage(
                "Clínica Psicología: Nuevo mensaje de contacto",
                "De {} <{}>\n\nEscribió:\n\n{}".format(name, email, content),
                "no-contestar@inbox.mailtrap.io",
                ['webseocordoba@gmail.com'],
                reply_to=[email]
            )
            try:
                email.send()
                # Todo ha ido bien y rediccionamos a ok
                return redirect(reverse('contact') + "?ok")
            except:
                # algo no ha ido bien y rediccionamos a FAIL

                return redirect(reverse('contact') + "?fail")




    return render(request, 'core/contact.html', {
        'title': title,
        'form': contact_form
    })

