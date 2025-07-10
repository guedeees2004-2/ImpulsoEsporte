# appImpulsoEsporte/views/auth_views.py

from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.views.generic import CreateView
from django.urls import reverse_lazy

from appImpulsoEsporte.forms import CustomUserCreationForm


# View de login baseada na classe LoginView do Django
class LoginView(DjangoLoginView):
    template_name = 'registration/login.html'


# View de registro personalizada baseada em CreateView
class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    
    def form_invalid(self, form):
        """
        Se o formulário for inválido, manter o formulário com os dados POST
        """
        return self.render_to_response(self.get_context_data(form=form))


# View para logout do usuário
def user_logout(request):
    logout(request)
    return redirect('home')
