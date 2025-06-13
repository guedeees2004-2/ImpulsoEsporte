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

# Vamos importar as views de uma forma mais limpa

from impulse_esporte.appImpulsoEsporte.views import index, RegisterView, LoginView, user_logout, pagina_atleta


urlpatterns = [
    # 1. Rota da página inicial (index), agora com o nome 'home' para o redirect funcionar
    path("", index, name="home"),
    
    # 2. Novas rotas para autenticação
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', user_logout, name='logout'),
    path("atleta/", pagina_atleta, name="pagina_atleta"),  # <-- Adicione esta linha

    # 3. Rotas que você já tinha
    path("admin/", admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
]

# Sua configuração de arquivos estáticos e de mídia continua a mesma
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)