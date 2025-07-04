from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views import View

from ..forms import CustomUserCreationForm, CustomAuthenticationForm
from ..models import Equipe, EquipeDisponivel


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
