from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models

from ..models import Patrocinador, Usuario, Jogador, Equipe
from ..forms import PartidaForm

# Dados globais temporários (considere mover para o banco de dados)
patrocinadores = []  # Lista vazia - patrocinadores serão adicionados pelo usuário
equipes = []  # Lista vazia - equipes serão obtidas do banco de dados
partidas = [
    "15/04/2023 - Time X vs Time Y",
    "20/04/2023 - Time A vs Time B"
]


@login_required
def pagina_atleta(request):
    """
    Página principal do atleta - redireciona para o perfil específico do atleta.
    """
    # Verificar se o usuário é atleta
    if not request.user.is_authenticated or request.user.tipo_conta != 'atleta':
        return redirect('home')
    
    # Redirecionar para o perfil específico do atleta
    return redirect('visualizar_perfil_atleta', atleta_id=request.user.id)
    
    # Redirecionar para o perfil específico do atleta
    return redirect('visualizar_perfil_atleta', atleta_id=request.user.id)


def visualizar_perfil_atleta(request, atleta_id):
    """
    View para visualizar o perfil de um atleta específico.
    """
    global patrocinadores, partidas, equipes
    
    atleta = get_object_or_404(Usuario, id=atleta_id, tipo_conta='atleta')
    
    # Verificar se é o próprio atleta
    is_owner = request.user.is_authenticated and request.user == atleta
    
    # Se for o dono, permitir funcionalidades de gerenciamento
    if is_owner:
        # Detectar qual formulário mostrar baseado nos parâmetros GET
        mostrar_form_patrocinador = request.GET.get('adicionar_patrocinador') == 'true'
        mostrar_form_partida = request.GET.get('adicionar_partida') == 'true'
        
        # Inicializar formulário de partida
        form = None
        if mostrar_form_partida:
            form = PartidaForm()
        
        if request.method == "POST":
            # Adicionar novo patrocinador
            if 'adicionar_patrocinador' in request.POST:
                novo_patrocinador = request.POST.get('novo_patrocinador', '').strip()
                if novo_patrocinador and novo_patrocinador not in patrocinadores:
                    patrocinadores.append(novo_patrocinador)
                    messages.success(request, 'Patrocinador adicionado com sucesso!')
                return redirect('visualizar_perfil_atleta', atleta_id=atleta.id)
            
            # Processar formulário de partida
            elif mostrar_form_partida or 'data' in request.POST:
                form = PartidaForm(request.POST)
                if form.is_valid():
                    # Por enquanto, adicionar à lista global (pode ser melhorado para salvar no banco)
                    partida_str = f"{form.cleaned_data['data'].strftime('%d/%m/%Y')} - {form.cleaned_data['adversario']}"
                    if partida_str not in partidas:
                        partidas.append(partida_str)
                        messages.success(request, 'Partida adicionada com sucesso!')
                    return redirect('visualizar_perfil_atleta', atleta_id=atleta.id)
                else:
                    # Se há erros, manter o formulário visível
                    mostrar_form_partida = True
            
            # Remover itens
            elif 'remover' in request.POST:
                item = request.POST.get('item')
                lista = request.POST.get('lista')
                
                if lista == 'patrocinadores' and item in patrocinadores:
                    patrocinadores.remove(item)
                    messages.success(request, 'Patrocinador removido com sucesso!')
                elif lista == 'partidas' and item in partidas:
                    partidas.remove(item)
                    messages.success(request, 'Partida removida com sucesso!')
                
                return redirect('visualizar_perfil_atleta', atleta_id=atleta.id)
    else:
        # Para visitantes, não mostrar formulários
        mostrar_form_patrocinador = False
        mostrar_form_partida = False
        form = None
    
    # Buscar a equipe do atleta (sempre visível para todos)
    atleta_equipe = None
    try:
        jogador = Jogador.objects.get(usuario=atleta)
        atleta_equipe = jogador.equipe
    except Jogador.DoesNotExist:
        pass
    
    # Buscar patrocinadores vinculados ao atleta (sempre visível para todos)
    patrocinadores_atleta = []
    
    # Buscar patrocinadores via PatrocinioJogador (se o atleta tem registro como Jogador)
    try:
        jogador = Jogador.objects.get(usuario=atleta)
        from ..models import PatrocinioJogador
        patrocinios_jogador = PatrocinioJogador.objects.filter(jogador=jogador).select_related('patrocinador')
        for patrocinio in patrocinios_jogador:
            patrocinadores_atleta.append(patrocinio.patrocinador)
    except Jogador.DoesNotExist:
        pass
    
    # Buscar patrocinadores via PatrocinioAtleta (se o atleta tem registro como Atleta)
    try:
        from ..models import Atleta, PatrocinioAtleta
        atleta_obj = Atleta.objects.get(usuario=atleta)
        patrocinios_atleta = PatrocinioAtleta.objects.filter(Atleta=atleta_obj).select_related('patrocinador')
        for patrocinio in patrocinios_atleta:
            if patrocinio.patrocinador not in patrocinadores_atleta:
                patrocinadores_atleta.append(patrocinio.patrocinador)
    except Atleta.DoesNotExist:
        pass
    
    context = {
        'atleta': atleta,
        'is_owner': is_owner,
        'user_type': getattr(request.user, 'tipo_conta', None) if request.user.is_authenticated else None,
        'title': f'Perfil de {atleta.first_name or atleta.username} - Impulso Esporte',
        'patrocinadores': sorted(patrocinadores) if is_owner else [],  # Lista global para o dono
        'patrocinadores_reais': patrocinadores_atleta,  # Patrocinadores reais do banco sempre visíveis
        'partidas': sorted(partidas) if is_owner else [],
        'equipes': equipes if is_owner else [],
        'atleta_equipe': atleta_equipe,  # Equipe sempre visível
        'mostrar_form_patrocinador': mostrar_form_patrocinador if is_owner else False,
        'mostrar_form_partida': mostrar_form_partida if is_owner else False,
        'form': form or PartidaForm() if is_owner else None,
    }
    
    return render(request, 'PaginaAtleta.html', context)


def lista_atletas(request):
    """
    View para listar atletas disponíveis para visualização de perfil.
    """
    from django.urls import reverse
    
    atletas = Usuario.objects.filter(tipo_conta='atleta')
    
    # Filtro de busca
    search_query = request.GET.get('search', '')
    if search_query:
        atletas = atletas.filter(
            models.Q(username__icontains=search_query) |
            models.Q(first_name__icontains=search_query) |
            models.Q(last_name__icontains=search_query)
        )
    
    # Lógica inteligente para o botão voltar
    referer = request.META.get('HTTP_REFERER', '/')
    current_url = request.build_absolute_uri()
    lista_atletas_url = request.build_absolute_uri(reverse('lista_atletas'))
    
    # Se o referer é a própria página de lista de atletas ou está vazio, usar página inicial
    if not referer or referer == current_url or lista_atletas_url in referer:
        back_url = reverse('home')
    else:
        back_url = referer
    
    context = {
        'atletas': atletas,
        'search_query': search_query,
        'user_type': getattr(request.user, 'tipo_conta', None) if request.user.is_authenticated else None,
        'title': 'Lista de Atletas - Impulso Esporte',
        'back_url': back_url,
    }
    
    return render(request, 'lista_atletas.html', context)
