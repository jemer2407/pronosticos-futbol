from django.urls import path
from . import views


urlpatterns = [
    path('', views.process_subscription, name="payment-subscription"),
    path('success/', views.success_payment, name="success-payment"),
    path('cancel/', views.cancel_payment, name="cancel-payment"),
    path('error/', views.error_payment, name="error-payment"),
]