from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.urls import reverse_lazy

from registration.models import Profile


class SubscriptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)


        if request.user.is_authenticated and not request.user.is_staff:
            profile = Profile.objects.get(user=request.user)
            if request.user.profile.is_trial and request.user.profile.trial_month < timezone.now():
                # El periodo de prueba ha expirado
                # Actualizamos el estado de is_trial y ponemos trial_month en None
                profile.is_trial = False
                profile.trial_month = None
                profile.save()
                # Cerramos sesión
                logout(request)
                # Retornamos a login
                return redirect('login')
            elif request.user.profile.is_subscribed and request.user.profile.subscription_month < timezone.now():
                # La suscripción ha expirado
                # Actualizamos el estado de is_subscribed y ponemos subscription_month en None
                profile.is_subscribed = False
                profile.subscription_month = None
                profile.save()
                # Cerramos sesión
                logout(request)
                # Retornamos a login 
                return redirect('login')

        return response