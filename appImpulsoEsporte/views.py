# Arquivo views.py principal - Importa todas as views dos módulos separados
# Mantém compatibilidade com o urls.py existente

from .views.auth_views import RegisterView, LoginView, user_logout
from .views.main_views import index, contato, pagina_sobre_nos, servicos
from .views.atleta_views import pagina_atleta, visualizar_perfil_atleta, lista_atletas
from .views.equipe_views import (
    buscar_equipes, gerenciar_equipes, pagina_equipe, 
    buscar_times, pagina_equipe_disponivel, minha_equipe, visualizar_perfil_equipe
)
from .views.patrocinador_views import buscar_patrocinadores

# Manter todas as funções disponíveis para importação
__all__ = [
    'RegisterView', 'LoginView', 'user_logout',
    'index', 'contato', 'pagina_sobre_nos', 'servicos',
    'pagina_atleta', 'visualizar_perfil_atleta', 'lista_atletas',
    'buscar_equipes', 'gerenciar_equipes', 'pagina_equipe',
    'buscar_times', 'pagina_equipe_disponivel', 'minha_equipe', 'visualizar_perfil_equipe',
    'buscar_patrocinadores'
]
