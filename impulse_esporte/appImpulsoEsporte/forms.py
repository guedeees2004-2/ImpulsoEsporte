from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length=25,
        label="Nome de usuário",
        error_messages={
            'max_length': 'O nome de usuário deve ter no máximo 25 caracteres.',
            'unique': 'Este nome de usuário já está em uso.',
            'required': 'O nome de usuário é obrigatório.',
        },
        help_text="Máximo de 25 caracteres. Apenas letras, números e @ . + - __"
    )

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ("username", "email")

class CustomAuthenticationForm(AuthenticationForm):
    pass