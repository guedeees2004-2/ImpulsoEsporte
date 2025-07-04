from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import models

from ..models import EquipeDisponivel, Equipe


@login_required
def buscar_equipes(request):
    """
    View para buscar equipes disponíveis para novos atletas.
    """
    if request.user.tipo_conta != 'atleta':
        return redirect('home')
    
    equipes_disponiveis = EquipeDisponivel.objects.filter(aberta_para_atletas=True)
    
    # Filtros de busca
    search_query = request.GET.get('search', '')
    modalidade_filter = request.GET.get('modalidade', '')
    cidade_filter = request.GET.get('cidade', '')
    
    # Aplicar filtros
    if search_query:
        equipes_disponiveis = equipes_disponiveis.filter(
            models.Q(nome__icontains=search_query) |
            models.Q(modalidade__icontains=search_query) |
            models.Q(cidade__icontains=search_query) |
            models.Q(descricao__icontains=search_query)
        )
    
    if modalidade_filter:
        equipes_disponiveis = equipes_disponiveis.filter(modalidade__icontains=modalidade_filter)
    
    if cidade_filter:
        equipes_disponiveis = equipes_disponiveis.filter(cidade__icontains=cidade_filter)
    
    context = {
        'equipes': equipes_disponiveis,
        'search_query': search_query,
        'modalidade_filter': modalidade_filter,
        'cidade_filter': cidade_filter,
        'user_type': request.user.tipo_conta,
    }
    
    return render(request, 'buscar_equipes.html', context)


def gerenciar_equipes(request):
    """
    View para gerenciar equipes (CRUD).
    """
    if request.method == "POST":
        action = request.POST.get('action')
        if action == 'cadastrar':
            nome = request.POST.get('nome', '').strip()
            modalidade = request.POST.get('modalidade', '').strip()
            cidade = request.POST.get('cidade', '').strip()
            if nome and modalidade and cidade:
                EquipeDisponivel.objects.create(
                    nome=nome,
                    modalidade=modalidade,
                    cidade=cidade,
                    aberta_para_atletas=True
                )
        elif action == 'remover':
            nome_remover = request.POST.get('nome_remover', '').strip()
            if nome_remover:
                EquipeDisponivel.objects.filter(nome=nome_remover).delete()
        return redirect('gerenciar_equipes')

    equipes = EquipeDisponivel.objects.all()
    context = {
        'title': 'Gerenciar Equipes - Impulso Esporte',
        'equipes': equipes,
    }
    return render(request, 'gerenciar_equipes.html', context)


def pagina_equipe(request, equipe_id):
    """
    View para visualizar página de uma equipe específica.
    """
    equipe = get_object_or_404(Equipe, id=equipe_id)
    
    # Verificar se é o dono da equipe
    is_owner = request.user.is_authenticated and request.user == equipe.usuario
    
    context = {
        "title": f"Impulso Esporte - {equipe.nome}",
        "equipe": equipe,
        'is_owner': is_owner,
        'user_type': getattr(request.user, 'tipo_conta', None),
    }
    return render(request, 'paginaEquipe.html', context)


def buscar_times(request):
    """
    View para buscar times/equipes.
    """
    query = request.GET.get('q', '')
    if query:
        resultados = EquipeDisponivel.objects.filter(nome__icontains=query)
    else:
        resultados = EquipeDisponivel.objects.all()
    return render(request, 'buscar_times.html', {'resultados': resultados, 'query': query})


def pagina_equipe_disponivel(request, equipe_id):
    """
    View para visualizar página de uma equipe disponível.
    """
    equipe = get_object_or_404(EquipeDisponivel, id=equipe_id)
    
    # Verificar se é o dono da equipe
    is_owner = False
    if request.user.is_authenticated:
        try:
            equipe_oficial = Equipe.objects.get(nome=equipe.nome)
            is_owner = request.user == equipe_oficial.usuario
        except Equipe.DoesNotExist:
            is_owner = False
    
    context = {
        "title": f"Impulso Esporte - {equipe.nome}",
        "equipe": equipe,
        'is_owner': is_owner,
        'user_type': getattr(request.user, 'tipo_conta', None) if request.user.is_authenticated else None,
    }
    return render(request, 'paginaEquipe.html', context)


@login_required
def minha_equipe(request):
    """
    Página da equipe para o usuário logado do tipo 'equipe'.
    """
    if request.user.tipo_conta != 'equipe':
        return redirect('home')
    
    try:
        equipe = request.user.equipe
        context = {
            "title": f"Impulso Esporte - {equipe.nome}",
            "equipe": equipe,
            'is_owner': True,
            'user_type': request.user.tipo_conta,
        }
        return render(request, 'paginaEquipe.html', context)
    except AttributeError:
        context = {
            "title": "Impulso Esporte - Configurar Equipe",
            "error_message": "Você ainda não tem uma equipe configurada. Entre em contato com o suporte.",
            'is_owner': True,
            'user_type': request.user.tipo_conta,
        }
        return render(request, 'paginaEquipe.html', context)


def visualizar_perfil_equipe(request, equipe_id):
    """
    View para visualizar o perfil de uma equipe específica.
    """
    try:
        # Tentar buscar na tabela EquipeDisponivel primeiro
        equipe_disponivel = get_object_or_404(EquipeDisponivel, id=equipe_id)
        
        # Verificar se existe uma equipe relacionada no modelo Equipe
        try:
            equipe_oficial = Equipe.objects.get(nome=equipe_disponivel.nome)
            is_owner = request.user.is_authenticated and request.user == equipe_oficial.usuario
            equipe_data = {
                'nome': equipe_oficial.nome,
                'modalidade': equipe_oficial.esporte,
                'cidade': equipe_oficial.localizacao,
                'descricao': equipe_disponivel.descricao or 'Sem descrição disponível',
                'ano_fundacao': equipe_disponivel.ano_fundacao,
                'numero_atletas': equipe_disponivel.numero_atletas,
            }
        except Equipe.DoesNotExist:
            is_owner = False
            equipe_data = {
                'nome': equipe_disponivel.nome,
                'modalidade': equipe_disponivel.modalidade,
                'cidade': equipe_disponivel.cidade,
                'descricao': equipe_disponivel.descricao or 'Sem descrição disponível',
                'ano_fundacao': equipe_disponivel.ano_fundacao,
                'numero_atletas': equipe_disponivel.numero_atletas,
            }
    except EquipeDisponivel.DoesNotExist:
        # Se não encontrar, tentar buscar diretamente na tabela Equipe
        equipe_oficial = get_object_or_404(Equipe, id=equipe_id)
        is_owner = request.user.is_authenticated and request.user == equipe_oficial.usuario
        equipe_data = {
            'nome': equipe_oficial.nome,
            'modalidade': equipe_oficial.esporte,
            'cidade': equipe_oficial.localizacao,
            'descricao': 'Sem descrição disponível',
            'ano_fundacao': None,
            'numero_atletas': None,
        }
    
    context = {
        'equipe': type('obj', (object,), equipe_data),  # Criar objeto dinâmico
        'is_owner': is_owner,
        'user_type': getattr(request.user, 'tipo_conta', None) if request.user.is_authenticated else None,
        'title': f'{equipe_data["nome"]} - Impulso Esporte',
    }
    
    return render(request, 'paginaEquipe.html', context)
