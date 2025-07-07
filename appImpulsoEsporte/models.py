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

    def __str__(self):
        return self.username


class Equipe(models.Model):
    usuario = models.OneToOneField('Usuario', on_delete=models.CASCADE, related_name='equipe', null=True, blank=True)
    nome = models.CharField(max_length=100)
    esporte = models.CharField(max_length=100)
    localizacao = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Jogador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    posicao = models.CharField(max_length=50)
    idade = models.PositiveIntegerField()
    esporte = models.ForeignKey(Esporte, on_delete=models.CASCADE)
    equipe = models.ForeignKey(Equipe, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.usuario.username


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


class PatrocinioJogador(models.Model):
    patrocinador = models.ForeignKey(Patrocinador, on_delete=models.CASCADE)
    jogador = models.ForeignKey(Jogador, on_delete=models.CASCADE)


class EquipeDisponivel(models.Model):
    """
    Modelo para equipes que estão abertas para novos atletas
    """
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
    aberta_para_atletas = models.BooleanField(
        default=True,
        verbose_name="Aberta para novos atletas",
        help_text="Indica se a equipe está recrutando novos membros"
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
