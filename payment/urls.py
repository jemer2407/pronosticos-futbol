from django.urls import path
from . import views


urlpatterns = [
    path('', views.checkout_session, name="checkout-session"),
    path('success/', views.success_payment, name="success"),
    path('subscriptions/', views.suscriptions, name="subscriptions"),
    path('cancel/', views.cancel_payment, name="cancel"),
    path('error/', views.error_payment, name="error"),
]