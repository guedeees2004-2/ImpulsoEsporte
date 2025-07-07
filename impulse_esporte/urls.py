from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from appImpulsoEsporte import views
from appImpulsoEsporte.views.patrocinador_views import listar_patrocinadores_publicos  

urlpatterns = [
    path("", views.index, name="home"),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.user_logout, name='logout'),
    path("atleta/", views.pagina_atleta, name="pagina_atleta"),
    path("atleta/<int:atleta_id>/", views.visualizar_perfil_atleta, name="visualizar_perfil_atleta"),
    path("atletas/", views.lista_atletas, name="lista_atletas"),
    path("minha-equipe/", views.minha_equipe, name="minha_equipe"),
    path("equipe/<int:equipe_id>/", views.visualizar_perfil_equipe, name="visualizar_perfil_equipe"),
    path("equipes/", views.buscar_times, name="lista_equipes"),
    path("patrocinadores/", views.buscar_patrocinadores, name="buscar_patrocinadores"),
    path("patrocinadores/publico/", listar_patrocinadores_publicos, name="pagina_patrocinadores"),  
    path("equipes/buscar/", views.buscar_equipes, name="buscar_equipes"),
    path("contato/", views.contato, name="contato"),
    path("admin/", admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path("equipe-disponivel/<int:equipe_id>/", views.pagina_equipe_disponivel, name="paginaEquipe"),
    path("sobre_nos", views.pagina_sobre_nos, name="pagina_sobre_nos"),
    path("gerenciar_equipes/", views.gerenciar_equipes, name="gerenciar_equipes"),
    path("buscar-times/", views.buscar_times, name="buscar_times"),
    path("servicos/", views.servicos, name="servicos"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)