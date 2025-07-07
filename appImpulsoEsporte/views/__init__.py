# Views modulares do Impulso Esporte
from .auth_views import RegisterView, LoginView, user_logout
from .main_views import index, contato, pagina_sobre_nos, servicos
from .atleta_views import pagina_atleta, visualizar_perfil_atleta, lista_atletas
from .equipe_views import (
    buscar_equipes, gerenciar_equipes, pagina_equipe, 
    buscar_times, pagina_equipe_disponivel, minha_equipe, visualizar_perfil_equipe,listar_atletas_da_equipe,adicionar_partida,
)
from .patrocinador_views import buscar_patrocinadores

# Exportar todas as views para manter compatibilidade
__all__ = [
    'RegisterView', 'LoginView', 'user_logout',
    'index', 'contato', 'pagina_sobre_nos', 'servicos',
    'pagina_atleta', 'visualizar_perfil_atleta', 'lista_atletas',
    'buscar_equipes', 'gerenciar_equipes', 'pagina_equipe',
    'buscar_times', 'pagina_equipe_disponivel', 'minha_equipe', 'visualizar_perfil_equipe',
    'buscar_patrocinadores','listar_atletas_da_equipe', 'adicionar_partida',
]
