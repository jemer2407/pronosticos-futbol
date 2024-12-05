"""
URL configuration for PronosticadorFutbol project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('', include('emailmarketing.urls')),
    path('pages/', include('pages.urls')),
    path('feeder/', include('feeder.urls')),
    path('forecasts/', include('forecasts.urls')),
    # paths de Auth. con este path django nos provee de varias urls para manejar autenticacion
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('registration.urls')),    
    path('summernote/', include('django_summernote.urls')),
    
]
if settings.DEBUG:
    from django.conf.urls.static import static
    # variables MEDIA_URL Y MEDIA_ROOT las tenemos que declarar en el settings del proyecto
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
