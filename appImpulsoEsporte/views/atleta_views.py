from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import models

from ..models import Patrocinador, Usuario

# Dados globais temporários (considere mover para o banco de dados)
patrocinadores = ["Nike", "Adidas", "Puma"]
equipes = ["Time A", "Time B", "Time C"]
partidas = [
    "15/04/2023 - Time X vs Time Y",
    "20/04/2023 - Time A vs Time B"
]


@login_required
def pagina_atleta(request):
    """
    Página principal do atleta com informações e funcionalidades básicas.
    """
    global patrocinadores, partidas, equipes
    
    # Verificar se o usuário é atleta
    if not request.user.is_authenticated or request.user.tipo_conta != 'atleta':
        return redirect('home')
    
    filtro_equipe = request.GET.get('filtro_equipe', '')
    box_aberto = request.GET.get('box_aberto', '')
    
    if request.method == "POST":
        # Adicionar novo patrocinador
        if 'adicionar_patrocinador' in request.POST:
            novo_patrocinador = request.POST.get('novo_patrocinador', '').strip()
            if novo_patrocinador and novo_patrocinador not in patrocinadores:
                patrocinadores.append(novo_patrocinador)
                box_aberto = 'patrocinador'
        
        # Adicionar nova partida
        elif 'adicionar_partida' in request.POST:
            nova_partida = request.POST.get('nova_partida', '').strip()
            if nova_partida and nova_partida not in partidas:
                partidas.append(nova_partida)
                box_aberto = 'partida'
        
        # Remover itens
        elif 'remover' in request.POST:
            item = request.POST.get('item')
            lista = request.POST.get('lista')
            
            if lista == 'patrocinadores' and item in patrocinadores:
                patrocinadores.remove(item)
            elif lista == 'partidas' and item in partidas:
                partidas.remove(item)
            
            box_aberto = lista[:-1]  # Remove o 's' final
        
        return redirect(f'{request.path}?box_aberto={box_aberto}')
    
    # Filtra equipes se houver filtro
    equipes_filtradas = [e for e in equipes if filtro_equipe.lower() in e.lower()]
    
    # Buscar patrocinadores disponíveis do banco de dados
    patrocinadores_disponiveis = Patrocinador.objects.filter(
        usuario__tipo_conta='patrocinador',
        aberto_para_oportunidades=True
    ).select_related('usuario')[:5]
    
    context = {
        'atleta': request.user,
        'is_owner': True,
        'patrocinadores': sorted(patrocinadores),
        'patrocinadores_disponiveis': patrocinadores_disponiveis,
        'equipes': sorted(equipes_filtradas if filtro_equipe else equipes),
        'partidas': sorted(partidas),
        'filtro_equipe': filtro_equipe,
        'box_aberto': box_aberto,
        'user_type': request.user.tipo_conta,
    }
    return render(request, 'PaginaAtleta.html', context)


def visualizar_perfil_atleta(request, atleta_id):
    """
    View para visualizar o perfil de um atleta específico.
    """
    atleta = get_object_or_404(Usuario, id=atleta_id, tipo_conta='atleta')
    
    # Verificar se é o próprio atleta
    is_owner = request.user.is_authenticated and request.user == atleta
    
    context = {
        'atleta': atleta,
        'is_owner': is_owner,
        'user_type': getattr(request.user, 'tipo_conta', None) if request.user.is_authenticated else None,
        'title': f'Perfil de {atleta.first_name or atleta.username} - Impulso Esporte',
        'patrocinadores': patrocinadores if is_owner else [],
        'partidas': partidas if is_owner else [],
        'equipes': equipes if is_owner else [],
    }
    
    return render(request, 'PaginaAtleta.html', context)


def lista_atletas(request):
    """
    View para listar atletas disponíveis para visualização de perfil.
    """
    atletas = Usuario.objects.filter(tipo_conta='atleta')
    
    # Filtro de busca
    search_query = request.GET.get('search', '')
    if search_query:
        atletas = atletas.filter(
            models.Q(username__icontains=search_query) |
            models.Q(first_name__icontains=search_query) |
            models.Q(last_name__icontains=search_query)
        )
    
    context = {
        'atletas': atletas,
        'search_query': search_query,
        'user_type': getattr(request.user, 'tipo_conta', None) if request.user.is_authenticated else None,
        'title': 'Lista de Atletas - Impulso Esporte',
    }
    
    return render(request, 'lista_atletas.html', context)
