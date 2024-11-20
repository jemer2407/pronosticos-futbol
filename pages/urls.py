from django.urls import path
from pages import views

urlpatterns = [
    path('page/<int:page_id>/<slug:page_slug>', views.page, name='page'),    
]
