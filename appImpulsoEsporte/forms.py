from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario
from .models import Partida

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
        label="Tipo de Conta",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # Campos condicionais
    esporte = forms.CharField(required=False, label="Tipo de Esporte")
    localizacao = forms.CharField(required=False, label="Localização")
    empresa = forms.CharField(required=False, label="Nome da Empresa")
    cnpj = forms.CharField(required=False, label="CNPJ")
    site_empresa = forms.URLField(required=False, label="Site da Empresa")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Sempre manter todos os campos, mas marcar como não obrigatórios inicialmente
        self.fields['esporte'].required = False
        self.fields['localizacao'].required = False
        self.fields['empresa'].required = False
        self.fields['cnpj'].required = False
        self.fields['site_empresa'].required = False

    def clean(self):
        cleaned_data = super().clean()
        tipo_conta = cleaned_data.get('tipo_conta')
        
        # Aplicar validação condicional baseada no tipo de conta
        if tipo_conta == 'equipe':
            if not cleaned_data.get('esporte'):
                self.add_error('esporte', 'Campo obrigatório para equipes.')
            if not cleaned_data.get('localizacao'):
                self.add_error('localizacao', 'Campo obrigatório para equipes.')
        elif tipo_conta == 'patrocinador':
            if not cleaned_data.get('empresa'):
                self.add_error('empresa', 'Campo obrigatório para patrocinadores.')
            if not cleaned_data.get('cnpj'):
                self.add_error('cnpj', 'Campo obrigatório para patrocinadores.')
            if not cleaned_data.get('site_empresa'):
                self.add_error('site_empresa', 'Campo obrigatório para patrocinadores.')
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.tipo_conta = self.cleaned_data['tipo_conta']
        if commit:
            user.save()
        return user

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ("username", "email", "tipo_conta", "password1", "password2")

class CustomAuthenticationForm(AuthenticationForm):
    pass
    
class PartidaForm(forms.ModelForm):
    class Meta:
        model = Partida
        fields = ['data', 'horario', 'adversario', 'local']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'horario': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'adversario': forms.TextInput(attrs={'placeholder': 'Adversário', 'class': 'form-control'}),
            'local': forms.TextInput(attrs={'placeholder': 'Local da partida', 'class': 'form-control'}),
        }
