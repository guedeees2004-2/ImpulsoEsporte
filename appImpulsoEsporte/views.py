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

def pagina_atleta(request):
    return render(request, "PaginaAtleta.html")