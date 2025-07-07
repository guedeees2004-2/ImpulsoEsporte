from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth import logout
from django.shortcuts import redirect
from appImpulsoEsporte.forms import CustomUserCreationForm
from django.views.generic import CreateView


class LoginView(DjangoLoginView):
    template_name = 'registration/login.html'


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = '/login/'


def user_logout(request):
    logout(request)
    return redirect('home')
