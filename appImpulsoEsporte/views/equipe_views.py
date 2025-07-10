from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import models
from django.contrib.auth import login
from django.contrib import messages

from ..models import EquipeDisponivel, Equipe, Jogador, Usuario
from ..models import Patrocinador, PatrocinioEquipe
from ..models import Jogador
from appImpulsoEsporte.forms import PartidaForm
from ..models import Partida



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
    View para gerenciar equipes (CRUD) e criar contas de usuário do tipo equipe.
    """
    form_data = {}
    form_errors = {}
    
    if request.method == "POST":
        action = request.POST.get('action')
        
        # Preservar dados do formulário para reexibir em caso de erro
        form_data = {
            'nome': request.POST.get('nome', '').strip(),
            'modalidade': request.POST.get('modalidade', '').strip(),
            'cidade': request.POST.get('cidade', '').strip(),
            'criar_usuario': request.POST.get('criar_usuario') == 'on',
            'username': request.POST.get('username', '').strip(),
            'email': request.POST.get('email', '').strip(),
            'password1': request.POST.get('password1', '').strip(),
            'password2': request.POST.get('password2', '').strip(),
        }
        
        if action == 'cadastrar':
            # Validação dos campos obrigatórios da equipe
            if not form_data['nome']:
                form_errors['nome'] = 'Nome da equipe é obrigatório.'
            if not form_data['modalidade']:
                form_errors['modalidade'] = 'Modalidade é obrigatória.'
            if not form_data['cidade']:
                form_errors['cidade'] = 'Cidade é obrigatória.'
                
            # Se solicitado criar usuário, validar campos do usuário
            if form_data['criar_usuario']:
                if not form_data['username']:
                    form_errors['username'] = 'Nome de usuário é obrigatório.'
                elif Usuario.objects.filter(username=form_data['username']).exists():
                    form_errors['username'] = 'Este nome de usuário já está em uso.'
                    
                if not form_data['email']:
                    form_errors['email'] = 'E-mail é obrigatório.'
                elif Usuario.objects.filter(email=form_data['email']).exists():
                    form_errors['email'] = 'Este e-mail já está em uso.'
                    
                if not form_data['password1']:
                    form_errors['password1'] = 'Senha é obrigatória.'
                elif len(form_data['password1']) < 8:
                    form_errors['password1'] = 'A senha deve ter pelo menos 8 caracteres.'
                    
                if not form_data['password2']:
                    form_errors['password2'] = 'Confirmação de senha é obrigatória.'
                elif form_data['password1'] != form_data['password2']:
                    form_errors['password2'] = 'As senhas não coincidem.'
            
            # Se não há erros, processar o cadastro
            if not form_errors:
                try:
                    # Criar a equipe disponível
                    equipe_disponivel = EquipeDisponivel.objects.create(
                        nome=form_data['nome'],
                        modalidade=form_data['modalidade'],
                        cidade=form_data['cidade'],
                        aberta_para_atletas=True
                    )
                    
                    # Se solicitado, criar também um usuário do tipo equipe
                    if form_data['criar_usuario']:
                        # Criar o usuário
                        usuario = Usuario.objects.create_user(
                            username=form_data['username'],
                            email=form_data['email'],
                            password=form_data['password1'],
                            tipo_conta='equipe'
                        )
                        
                        # Criar a equipe oficial vinculada ao usuário
                        Equipe.objects.create(
                            usuario=usuario,
                            nome=form_data['nome'],
                            esporte=form_data['modalidade'],
                            localizacao=form_data['cidade']
                        )
                        
                        messages.success(request, f'Equipe "{form_data["nome"]}" e conta de usuário criadas com sucesso!')
                    else:
                        messages.success(request, f'Equipe "{form_data["nome"]}" cadastrada com sucesso!')
                        
                    return redirect('gerenciar_equipes')
                    
                except Exception as e:
                    messages.error(request, f'Erro ao criar equipe/usuário: {str(e)}')
                    
        elif action == 'remover':
            nome_remover = request.POST.get('nome_remover', '').strip()
            if nome_remover:
                EquipeDisponivel.objects.filter(nome=nome_remover).delete()
                messages.success(request, f'Equipe "{nome_remover}" removida com sucesso!')
                return redirect('gerenciar_equipes')

    # GET request - listar equipes e mostrar formulário
    equipes = EquipeDisponivel.objects.all()
    editar_equipe_nome = request.GET.get('editar')
    editar_equipe = None
    
    if editar_equipe_nome:
        try:
            editar_equipe = EquipeDisponivel.objects.get(nome=editar_equipe_nome)
        except EquipeDisponivel.DoesNotExist:
            pass
    
    context = {
        'title': 'Gerenciar Equipes - Impulso Esporte',
        'equipes': equipes,
        'editar_equipe': editar_equipe,
        'form_data': form_data,
        'form_errors': form_errors,
    }
    return render(request, 'gerenciar_equipes.html', context)


def pagina_equipe(request, equipe_id):
    equipe = get_object_or_404(Equipe, id=equipe_id)
    is_owner = request.user.is_authenticated and request.user == equipe.usuario

    # Buscar os patrocinadores vinculados a essa equipe
    patrocinios = PatrocinioEquipe.objects.filter(equipe=equipe).select_related('patrocinador')
    patrocinadores = [p.patrocinador for p in patrocinios]

    # Buscar os jogadores vinculados à equipe
    jogadores = Jogador.objects.filter(equipe=equipe)

    context = {
        "title": f"Impulso Esporte - {equipe.nome}",
        "equipe": equipe,
        "jogadores": jogadores,  
        'is_owner': is_owner,
        'user_type': getattr(request.user, 'tipo_conta', None),
        'patrocinadores': patrocinadores,
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
    usuario = request.user

    try:
        equipe = Equipe.objects.get(usuario=usuario)
    except Equipe.DoesNotExist:
        return redirect("home")

    jogadores = Jogador.objects.filter(equipe=equipe)
    patrocinadores = Patrocinador.objects.filter(patrocinioequipe__equipe=equipe).distinct()
    partidas = Partida.objects.filter(equipe=equipe).order_by('data', 'horario')

    mostrar_form_partida = request.GET.get('inline') == 'true'
    form = PartidaForm(request.POST or None)

    if request.method == 'POST' and mostrar_form_partida and form.is_valid():
        partida = form.save(commit=False)
        partida.equipe = equipe
        partida.save()
        return redirect('minha_equipe')

    context = {
        "equipe": equipe,
        "is_owner": True,
        "jogadores": jogadores,
        "patrocinadores": patrocinadores,
        "partidas": partidas,
        "form": form if mostrar_form_partida else None,
        "mostrar_form_partida": mostrar_form_partida,
    }

    return render(request, "paginaEquipe.html", context)


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
from ..models import Jogador

@login_required
def listar_atletas_da_equipe(request, equipe_id):
    equipe = get_object_or_404(Equipe, id=equipe_id)
    atletas = Jogador.objects.filter(equipe=equipe)
    context = {
        'equipe': equipe,
        'atletas': atletas,
    }
    return render(request, 'lista_atletas.html', context)

@login_required
def adicionar_partida(request, equipe_id):
    equipe = get_object_or_404(Equipe, id=equipe_id)

    if request.method == "POST":
        form = PartidaForm(request.POST)
        if form.is_valid():
            partida = form.save(commit=False)
            partida.equipe = equipe
            partida.save()
            return redirect('minha_equipe')  # ou 'paginaEquipe', equipe_id=equipe.id
    else:
        form = PartidaForm()

    return render(request, 'form_partida.html', {'form': form, 'equipe': equipe})

@login_required
def editar_partida(request, equipe_id, partida_id):
    equipe = get_object_or_404(Equipe, id=equipe_id)
    partida = get_object_or_404(Partida, id=partida_id, equipe=equipe)

    if request.method == "POST":
        form = PartidaForm(request.POST, instance=partida)
        if form.is_valid():
            form.save()
            return redirect('minha_equipe')
    else:
        form = PartidaForm(instance=partida)

    return render(request, 'form_partida.html', {'form': form, 'equipe': equipe, 'editar': True})

@login_required
def excluir_partida(request, equipe_id, partida_id):
    equipe = get_object_or_404(Equipe, id=equipe_id)
    partida = get_object_or_404(Partida, id=partida_id, equipe=equipe)

    if request.method == "POST":
        partida.delete()
        return redirect('minha_equipe')

    return render(request, 'confirmar_exclusao.html', {'partida': partida, 'equipe': equipe})
