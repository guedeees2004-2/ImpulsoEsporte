from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ..models import Patrocinador


@login_required
def buscar_patrocinadores(request):
    """
    View para buscar patrocinadores disponíveis.
    Acessível apenas para usuários do tipo 'atleta' ou 'equipe'.
    """
    # Verificar se o usuário é atleta ou equipe
    if request.user.tipo_conta not in ['atleta', 'equipe']:
        return redirect('home')
    
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
        'user_type': request.user.tipo_conta,
    }
    
    return render(request, 'buscar_patrocinadores.html', context)
