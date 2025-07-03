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

    tipo_conta = forms.ChoiceField(
        choices=Usuario.TIPOS_USUARIO,
        label="Tipo de Conta"
    )
    esporte = forms.CharField(required=False, label="Tipo de Esporte")
    localizacao = forms.CharField(required=False, label="Localização")
    cnpj = forms.CharField(required=False, label="CNPJ")

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ("username", "email", "tipo_conta", "esporte", "localizacao", "cnpj", "password1", "password2")

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get("tipo_conta")
        if tipo == "equipe":
            if not cleaned_data.get("esporte"):
                self.add_error("esporte", "Campo obrigatório para equipes.")
            if not cleaned_data.get("localizacao"):
                self.add_error("localizacao", "Campo obrigatório para equipes.")
        if tipo == "patrocinador":
            if not cleaned_data.get("cnpj"):
                self.add_error("cnpj", "Campo obrigatório para patrocinadores.")
        return cleaned_data

class CustomAuthenticationForm(AuthenticationForm):
    pass