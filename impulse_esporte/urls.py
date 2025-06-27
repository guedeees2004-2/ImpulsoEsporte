"""
URL configuration for impulse_esporte project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf.urls.static import static

from appImpulsoEsporte.views import index, RegisterView, LoginView, user_logout, pagina_atleta, buscar_patrocinadores, contato, buscar_equipes, gerenciar_equipes, lista_equipes


urlpatterns = [
    path("", index, name="home"),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', user_logout, name='logout'),
    path("atleta/", pagina_atleta, name="pagina_atleta"),
    path("patrocinadores/", buscar_patrocinadores, name="buscar_patrocinadores"),
    path("equipes/buscar/", buscar_equipes, name="buscar_equipes"),
    path("contato/", contato, name="contato"),
    path("admin/", admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)