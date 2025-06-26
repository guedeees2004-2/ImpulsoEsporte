from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views import View

from .forms import CustomUserCreationForm, CustomAuthenticationForm



def index(request):
    context = {
        "title": "Impulse Esporte",
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

def pagina_atleta(request):
    global patrocinadores, partidas, equipes
    
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
    
    context = {
        'patrocinadores': sorted(patrocinadores),
        'equipes': sorted(equipes_filtradas if filtro_equipe else equipes),
        'partidas': sorted(partidas),
        'filtro_equipe': filtro_equipe,
        'box_aberto': box_aberto,
    }
    return render(request, 'PaginaAtleta.html', context)