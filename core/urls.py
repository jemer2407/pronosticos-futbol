from django.urls import path
from .views import HomeView, AboutView, contact

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('about/', AboutView.as_view(), name="about"),
    path('contact/', contact, name="contact"),
]