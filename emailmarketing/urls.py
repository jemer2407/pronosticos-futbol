from django.urls import path
from . import views

urlpatterns = [
    #urls de emailmarketing
    
    path('subscribers/create', views.SubscriberCreateView.as_view(), name='subscriber-create'),
    path('subscribers/maintenance/', views.SubscriberListView.as_view(), name='subscribers-list'),
    path('subscribers/maintenance/create/', views.LoginSubscriberCreateView.as_view(), name='subscriber-maintenance-create'),
    path('subscribers/maintenance/update/<int:pk>/', views.SubscriberUpdateView.as_view(), name='subscriber-update'),
    path('subscribers/maintenance/delete/<int:pk>/', views.SubscriberDeleteView.as_view(), name='subscriber-delete'),
    path('subscribers/campaign/', views.emailMarketing, name='campaign-email-form'),
]

