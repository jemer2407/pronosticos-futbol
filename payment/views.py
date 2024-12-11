from django.shortcuts import render
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
import stripe


# Create your views here.


# This is your test secret API key.
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

def process_subscription(request):
    # Obtener la información del usuario y el plan de suscripción
    user = request.user  # Suponiendo que el usuario está autenticado
    price_id = '20'  # Reemplaza con el ID del precio de tu plan mensual en Stripe

    try:
        # Crear una sesión de suscripción
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer_email=user.email,
            line_items=[
                {
                    'price': price_id,
                    'quantity': 1,
                },
            ],
            mode='subscription',            
            success_url=reverse_lazy('success-payment'),
            cancel_url=reverse_lazy('cancel-payment')
        )
    except stripe.error.StripeError as e:
        # Manejar errores
        return render(request, 'payment/error.html', {'error': e.user_message})

    # Redirigir al usuario a la página de pago de Stripe
    return redirect(session.url, code=303)

def success_payment(request):
    render(request,'payment/success.html',{
        'title': 'Pago realizado'
    })

def cancel_payment(request):
    render(request,'payment/cancel.html',{
        'title': 'Pago cancelado'
    })

def error_payment(request):
    render(request,'error.html',{
        'title': 'Error en el Pago'
    })