from django.contrib.auth.models import AbstractUser
from django.db import models


class Esporte(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Usuario(AbstractUser):
    TIPOS_USUARIO = [
        ('', 'Selecione o tipo de conta'),
        ('atleta', 'Atleta'),
        ('patrocinador', 'Patrocinador'),
        ('equipe', 'Equipe'),
        ('outro', 'Outro'),
    ]
    tipo_conta = models.CharField(
        max_length=20,
        choices=TIPOS_USUARIO,
        default='atleta',
        verbose_name='Tipo de Conta'
    )
    tipo_usuario = models.CharField(max_length=20, choices=TIPOS_USUARIO)
    username = models.CharField(
        max_length=25,
        unique=True,
        verbose_name='nome de usuário'
    )

    def clean(self):
        """Validação customizada para impedir superusers de serem atletas"""
        from django.core.exceptions import ValidationError
        super().clean()
        
        if self.is_superuser and self.tipo_conta == 'atleta':
            raise ValidationError({
                'tipo_conta': 'Superusers não podem ter tipo de conta "atleta". Escolha outro tipo.'
            })
    
    def save(self, *args, **kwargs):
        """Override do save para garantir validação"""
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Equipe(models.Model):
    usuario = models.OneToOneField('Usuario', on_delete=models.CASCADE, related_name='equipe', null=True, blank=True)
    nome = models.CharField(max_length=100)
    esporte = models.CharField(max_length=100)
    localizacao = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


# Modelo Atleta representa os Atletas do sistema
class Atleta(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    posicao = models.CharField(max_length=50)
    idade = models.PositiveIntegerField()
    esporte = models.ForeignKey(Esporte, on_delete=models.CASCADE)
    equipe = models.ForeignKey(Equipe, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.usuario.username


# Modelo Jogador representa os Jogadores do sistema (similar ao Atleta, mas com estrutura diferente)
class Jogador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    posicao = models.CharField(max_length=50)
    idade = models.PositiveIntegerField()
    esporte = models.ForeignKey(Esporte, on_delete=models.CASCADE)
    equipe = models.ForeignKey(Equipe, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.usuario.username


class Partida(models.Model):
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE, related_name='partidas')
    data = models.DateField()
    horario = models.TimeField()
    adversario = models.CharField(max_length=100)
    local = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.equipe.nome} x {self.adversario} - {self.data}"


class Patrocinador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    empresa = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=20)
    descricao = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Descrição da empresa",
        help_text="Breve descrição sobre a empresa e o que oferece"
    )
    logo = models.ImageField(upload_to='logos_patrocinadores/', blank=True, null=True)
    site = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Site da empresa",
        help_text="Website oficial da empresa"
    )

    def __str__(self):
        return self.empresa


class PatrocinioEquipe(models.Model):
    patrocinador = models.ForeignKey(Patrocinador, on_delete=models.CASCADE)
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE)


class PatrocinioAtleta(models.Model):
    patrocinador = models.ForeignKey(Patrocinador, on_delete=models.CASCADE)
    Atleta = models.ForeignKey(Atleta, on_delete=models.CASCADE)


class PatrocinioJogador(models.Model):
    patrocinador = models.ForeignKey(Patrocinador, on_delete=models.CASCADE)
    jogador = models.ForeignKey(Jogador, on_delete=models.CASCADE)


class EquipeDisponivel(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome da Equipe")
    modalidade = models.CharField(max_length=50, verbose_name="Modalidade Esportiva")
    cidade = models.CharField(max_length=100, verbose_name="Cidade")
    descricao = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Descrição da equipe",
        help_text="Informações sobre a equipe, objetivos e requisitos"
    )
    ano_fundacao = models.PositiveIntegerField(
        blank=True, 
        null=True,
        verbose_name="Ano de Fundação"
    )
    numero_atletas = models.PositiveIntegerField(
        blank=True, 
        null=True,
        verbose_name="Número atual de atletas"
    )
    contato_responsavel = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Responsável pelo contato"
    )
    email_contato = models.EmailField(
        blank=True,
        null=True,
        verbose_name="Email para contato"
    )
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Equipe Disponível"
        verbose_name_plural = "Equipes Disponíveis"
        ordering = ['-data_atualizacao']
    
    def __str__(self):
        return f"{self.nome} - {self.modalidade} ({self.cidade})"
