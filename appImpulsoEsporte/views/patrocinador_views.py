from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ..models import Patrocinador


def buscar_patrocinadores(request):
    """
    View para buscar patrocinadores disponíveis.
    Acessível para todos os usuários (logados ou não).
    """
    # Buscar todos os patrocinadores
    patrocinadores_disponiveis = Patrocinador.objects.filter(
        usuario__tipo_conta='patrocinador'
    ).select_related('usuario')
    
    # Filtro de busca (opcional)
    search_query = request.GET.get('search', '')
    if search_query:
        patrocinadores_disponiveis = patrocinadores_disponiveis.filter(
            empresa__icontains=search_query
        )
    
    context = {
        'patrocinadores': patrocinadores_disponiveis,
        'search_query': search_query,
        'user_type': request.user.tipo_conta if request.user.is_authenticated else None,
    }
    
    return render(request, 'buscar_patrocinadores.html', context)
def listar_patrocinadores_publicos(request):
    """
    Página pública de patrocinadores com logo e link para o site.
    """
    patrocinadores = Patrocinador.objects.filter(aberto_para_oportunidades=True)
    
    context = {
        'patrocinadores': patrocinadores
    }
    
    return render(request, 'pagina_patrocinadores.html', context)
