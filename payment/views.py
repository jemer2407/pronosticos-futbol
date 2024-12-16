from django.shortcuts import render
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
import stripe
from decimal import Decimal
from django.utils import timezone
from registration.models import Profile


# Create your views here.


# This is your test secret API key.
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

def checkout_session(request):
    # Obtener la información del usuario y el plan de suscripción
    user = request.user  # Suponiendo que el usuario está autenticado
    
    try:
        # Crear una sesión de suscripción
        session = stripe.checkout.Session.create(
            payment_method_types=['card', 'paypal','revolut_pay'],
            customer_email=user.email,
            line_items=[
                {
                    'price_data': {
                        'currency': 'eur',
                        'unit_amount': 1000,
                        'product_data': {
                            'name': 'Basico',
                            'description': 'Suscribirse a Estratebet por un periodo de 30 días. Si se suscribe y aun tiene un periodo de prueba, éste lo perderá.'
                        }
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',            
            success_url=settings.DOMAIN + 'payment/success/',
            cancel_url=settings.DOMAIN + 'payment/cancel/'
        )
    except stripe.error.StripeError as e:
        # Manejar errores
        return render(request, 'payment/error.html', {'error': e.user_message})

    # Redirigir al usuario a la página de pago de Stripe
    return redirect(session.url, code=303)


def success_payment(request):
    profile = Profile.objects.get(user=request.user)
    profile.date_subscription = timezone.now()
    profile.subscription_month = timezone.now() + timezone.timedelta(minutes=20)
    profile.is_subscribed = True
    if profile.is_trial == True:
        profile.is_trial = False
        profile.trial_month = None
        
    profile.save()

    return render(request,'payment/success.html',{
        'title': 'Pago realizado con éxito'
    })

def cancel_payment(request):
    return render(request,'payment/cancel.html',{
        'title': 'Pago cancelado'
    })

def error_payment(request):
    return render(request,'error.html',{
        'title': 'Error en el Pago'
    })

def suscriptions(request):
    title = 'Suscripciones'
    return render(request,'payment/suscriptions.html', {
        'title': title
    })