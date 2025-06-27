from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views import View
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import models

from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import Patrocinador, Usuario, EquipeDisponivel



def index(request):
    context = {
        "title": "Impulso Esporte",
    }
    return render(request, "index.html", context)

class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  
        return render(request, 'registration/register.html', {'form': form})

class LoginView(View):
    def get(self, request):
        form = CustomAuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})

    def post(self, request):
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  
        return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return render(request, 'index.html')

patrocinadores = ["Nike", "Adidas", "Puma"]
equipes = ["Time A", "Time B", "Time C"]
partidas = [
    "15/04/2023 - Time X vs Time Y",
    "20/04/2023 - Time A vs Time B"
]

@login_required
def buscar_patrocinadores(request):
    """
    View para buscar patrocinadores disponíveis.
    Acessível apenas para usuários do tipo 'atleta' ou 'equipe'.
    """
    # Verificar se o usuário é atleta ou equipe
    if request.user.tipo_conta not in ['atleta', 'equipe']:
        return redirect('home')
    
    # Buscar patrocinadores que estão abertos para oportunidades
    patrocinadores_disponiveis = Patrocinador.objects.filter(
        usuario__tipo_conta='patrocinador',
        aberto_para_oportunidades=True
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


def pagina_atleta(request):
    """
    Página principal do atleta/equipe com informações e funcionalidades básicas.
    """
    global patrocinadores, partidas, equipes
    
    # Verificar se o usuário é atleta ou equipe
    if not request.user.is_authenticated or request.user.tipo_conta not in ['atleta', 'equipe']:
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
            
            box_aberto = lista[:-1]  # Remove o 's' final (patrocinadores -> patrocinador)
        
        return redirect(f'{request.path}?box_aberto={box_aberto}')
    
    # Filtra equipes se houver filtro
    equipes_filtradas = [e for e in equipes if filtro_equipe.lower() in e.lower()]
    
    # Buscar patrocinadores disponíveis do banco de dados
    patrocinadores_disponiveis = Patrocinador.objects.filter(
        usuario__tipo_conta='patrocinador',
        aberto_para_oportunidades=True
    ).select_related('usuario')[:5]  # Mostrar apenas os 5 primeiros
    
    context = {
        'patrocinadores': sorted(patrocinadores),
        'patrocinadores_disponiveis': patrocinadores_disponiveis,
        'equipes': sorted(equipes_filtradas if filtro_equipe else equipes),
        'partidas': sorted(partidas),
        'filtro_equipe': filtro_equipe,
        'box_aberto': box_aberto,
        'user_type': request.user.tipo_conta,
    }
    return render(request, 'PaginaAtleta.html', context)


def contato(request):
    context = {
        "title": "Impulso Esporte - Contato",
    }
    return render(request, "contato.html", context)

# Lista simulada de equipes para demonstração
equipes_cadastradas = [
    {"nome": "Dragões do Futsal", "modalidade": "Futsal", "cidade": "São Paulo", "ano_fundacao": "2018", "numero_membros": "25"},
    {"nome": "Águias do Vôlei", "modalidade": "Vôlei", "cidade": "Rio de Janeiro", "ano_fundacao": "2020", "numero_membros": "18"},
    {"nome": "Leões do Basquete", "modalidade": "Basquete", "cidade": "Belo Horizonte", "ano_fundacao": "2019", "numero_membros": "15"},
    {"nome": "Tubarões da Natação", "modalidade": "Natação", "cidade": "Porto Alegre", "ano_fundacao": "2017", "numero_membros": "12"},
    {"nome": "Falcões do Atletismo", "modalidade": "Atletismo", "cidade": "Recife", "ano_fundacao": "2021", "numero_membros": "20"},
]


def gerenciar_equipes(request):
    """
    View para gerenciar equipes - cadastrar e remover
    """
    global equipes_cadastradas
    
    if request.method == "POST":
        action = request.POST.get('action')
        
        if action == 'cadastrar':
            nome = request.POST.get('nome', '').strip()
            modalidade = request.POST.get('modalidade', '').strip()
            cidade = request.POST.get('cidade', '').strip()
            
            if nome and modalidade and cidade:
                # Verificar se a equipe já existe
                equipe_existe = any(equipe['nome'].lower() == nome.lower() for equipe in equipes_cadastradas)
                
                if not equipe_existe:
                    nova_equipe = {
                        "nome": nome,
                        "modalidade": modalidade,
                        "cidade": cidade,
                        "ano_fundacao": "2024",  # Ano atual como padrão
                        "numero_membros": "10"   # Número padrão
                    }
                    equipes_cadastradas.append(nova_equipe)
                    
        elif action == 'remover':
            nome_remover = request.POST.get('nome_remover', '').strip()
            if nome_remover:
                equipes_cadastradas[:] = [
                    equipe for equipe in equipes_cadastradas 
                    if equipe['nome'].lower() != nome_remover.lower()
                ]
        
        return redirect('gerenciar_equipes')
    
    context = {
        'title': 'Gerenciar Equipes - Impulso Esporte',
        'equipes': equipes_cadastradas,
    }
    return render(request, 'gerenciar_equipes.html', context)


def lista_equipes(request):
    """
    View para listar todas as equipes com filtros
    """
    global equipes_cadastradas
    
    # Obter filtros da URL
    search_query = request.GET.get('search', '').strip()
    modalidade_filter = request.GET.get('modalidade', '').strip()
    cidade_filter = request.GET.get('cidade', '').strip()
    
    # Filtrar equipes
    equipes_filtradas = equipes_cadastradas.copy()
    
    if search_query:
        equipes_filtradas = [
            equipe for equipe in equipes_filtradas
            if search_query.lower() in equipe['nome'].lower()
        ]
    
    if modalidade_filter:
        equipes_filtradas = [
            equipe for equipe in equipes_filtradas
            if modalidade_filter.lower() in equipe['modalidade'].lower()
        ]
    
    if cidade_filter:
        equipes_filtradas = [
            equipe for equipe in equipes_filtradas
            if cidade_filter.lower() in equipe['cidade'].lower()
        ]
    
    # Calcular estatísticas
    modalidades_unicas = set(equipe['modalidade'] for equipe in equipes_cadastradas)
    cidades_unicas = set(equipe['cidade'] for equipe in equipes_cadastradas)
    
    context = {
        'title': 'Lista de Equipes - Impulso Esporte',
        'equipes': equipes_filtradas,
        'search_query': search_query,
        'modalidade_filter': modalidade_filter,
        'cidade_filter': cidade_filter,
        'total_equipes': len(equipes_cadastradas),
        'total_modalidades': len(modalidades_unicas),
        'total_cidades': len(cidades_unicas),
    }
    return render(request, 'lista_equipes.html', context)

@login_required
def buscar_equipes(request):
    """
    View para buscar equipes disponíveis para novos atletas.
    Acessível apenas para usuários do tipo 'atleta'.
    """
    # Verificar se o usuário é atleta
    if request.user.tipo_conta != 'atleta':
        return redirect('home')
    
    # Buscar equipes que estão abertas para novos atletas
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

def pagina_sobre_nos(request):
    context = {
        "title": "Sobre Nós - Impulso Esporte",
    }
    return render(request, "paginaSobreNos.html", context)

def pagina_equipe(request):
    context = {
        "title ": "Impulso Esporte - Equipe",
    }
    return render(request, 'paginaEquipe.html', context)
