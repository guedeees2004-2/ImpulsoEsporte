from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.views import View
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import models

from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import Patrocinador, Usuario, EquipeDisponivel, Equipe



def index(request):
    context = {
        "title": "Impulso Esporte",
    }
    return render(request, "paginaPrincipal.html", context)

class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, "registration/register.html", {"form": form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            # Cria uma equipe se o usuário for do tipo equipe
            if usuario.tipo_conta == 'equipe':
                equipe = Equipe.objects.create(
                    usuario=usuario,
                    nome=usuario.username,
                    esporte=form.cleaned_data.get('esporte', ''),
                    localizacao=form.cleaned_data.get('localizacao', '')
                )
                # Cria também no EquipeDisponivel
                EquipeDisponivel.objects.create(
                    nome=equipe.nome,
                    modalidade=equipe.esporte,
                    cidade=equipe.localizacao,
                    aberta_para_atletas=True
                )
            return redirect("login")
        return render(request, "registration/register.html", {"form": form})

class LoginView(View):
    def get(self, request):
        form = CustomAuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})

    def post(self, request):
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirecionar baseado no tipo de conta
            if user.tipo_conta == 'atleta':
                return redirect('pagina_atleta')
            else:
                return redirect('home')
        return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return render(request, 'paginaPrincipal.html')

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
        'atleta': request.user,  # Adicionar o atleta atual
        'is_owner': True,  # Sempre True pois é a própria página do atleta
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




from .models import EquipeDisponivel

def gerenciar_equipes(request):
    editar_equipe = None
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
            # Remover por nome (do select) OU por nome do card
            nome_remover = request.POST.get('nome_remover', '').strip()
            if nome_remover:
                EquipeDisponivel.objects.filter(nome=nome_remover).delete()
        return redirect('gerenciar_equipes')

    equipes = EquipeDisponivel.objects.all()
    context = {
        'title': 'Gerenciar Equipes - Impulso Esporte',
        'equipes': equipes,
        'editar_equipe': editar_equipe,
    }
    return render(request, 'gerenciar_equipes.html', context)

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

def pagina_equipe(request, equipe_id):
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
    query = request.GET.get('q', '')
    if query:
        resultados = EquipeDisponivel.objects.filter(nome__icontains=query)
    else:
        resultados = EquipeDisponivel.objects.all()
    return render(request, 'buscar_times.html', {'resultados': resultados, 'query': query})

def pagina_equipes(request):
    equipes = Equipe.objects.all()
    return render(request, "pagina_equipes.html", {"equipes": equipes})

def pagina_equipe_disponivel(request, equipe_id):
    equipe = get_object_or_404(EquipeDisponivel, id=equipe_id)
    
    # Verificar se é o dono da equipe (se existir uma equipe oficial relacionada)
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
    # Verificar se o usuário é do tipo equipe
    if request.user.tipo_conta != 'equipe':
        return redirect('home')
    
    try:
        # Tentar encontrar a equipe do usuário
        equipe = request.user.equipe
        context = {
            "title": f"Impulso Esporte - {equipe.nome}",
            "equipe": equipe,
            'is_owner': True,  # Sempre True pois é a própria equipe do usuário
            'user_type': request.user.tipo_conta,
        }
        return render(request, 'paginaEquipe.html', context)
    except AttributeError:
        # Se o usuário não tem uma equipe associada, redirecionar ou mostrar mensagem
        context = {
            "title": "Impulso Esporte - Configurar Equipe",
            "error_message": "Você ainda não tem uma equipe configurada. Entre em contato com o suporte.",
            'is_owner': True,
            'user_type': request.user.tipo_conta,
        }
        return render(request, 'paginaEquipe.html', context)

def visualizar_perfil_atleta(request, atleta_id):
    """
    View para visualizar o perfil de um atleta específico.
    Qualquer usuário pode visualizar, mas apenas o próprio atleta pode editar.
    """
    atleta = get_object_or_404(Usuario, id=atleta_id, tipo_conta='atleta')
    
    # Verificar se é o próprio atleta (pode editar) ou visitante (apenas visualizar)
    is_owner = request.user.is_authenticated and request.user == atleta
    
    context = {
        'atleta': atleta,
        'is_owner': is_owner,
        'user_type': getattr(request.user, 'tipo_conta', None) if request.user.is_authenticated else None,
        'title': f'Perfil de {atleta.first_name or atleta.username} - Impulso Esporte',
        # Se for o dono, incluir dados editáveis
        'patrocinadores': patrocinadores if is_owner else [],  # Usar dados globais se for o dono
        'partidas': partidas if is_owner else [],  # Usar dados globais se for o dono
        'equipes': equipes if is_owner else [],  # Usar dados globais se for o dono
    }
    
    return render(request, 'PaginaAtleta.html', context)

def visualizar_perfil_equipe(request, equipe_id):
    """
    View para visualizar o perfil de uma equipe específica.
    Qualquer usuário pode visualizar, mas apenas membros da equipe podem editar.
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
            # Se não existe na tabela Equipe, é apenas uma equipe disponível
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

def lista_atletas(request):
    """
    View para listar atletas disponíveis para visualização de perfil.
    """
    # Buscar todos os atletas
    atletas = Usuario.objects.filter(tipo_conta='atleta')
    
    # Filtro de busca (opcional)
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