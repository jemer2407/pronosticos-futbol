
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.urls import reverse
from .forms import ContactForm
from django.core.mail import EmailMessage
from forecasts.models import Match, Contry, League



class HomeView(TemplateView):
    model = Match
    template_name = "core/home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Pronosticador Fútbol'
        leagues = League.objects.all()
        context['leagues'] = leagues


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

