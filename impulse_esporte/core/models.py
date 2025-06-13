from django.db import models
from django.contrib.auth.models import AbstractUser


class Esporte(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Usuario(AbstractUser):
    TIPOS_USUARIO = [
        ('jogador', 'Jogador'),
        ('patrocinador', 'Patrocinador'),
    ]
    tipo_usuario = models.CharField(max_length=20, choices=TIPOS_USUARIO)

    def __str__(self):
        return self.username


class Equipe(models.Model):
    nome_da_equipe = models.CharField(max_length=100)
    esporte = models.ForeignKey(Esporte, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome_da_equipe


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

    def __str__(self):
        return self.empresa


class PatrocinioEquipe(models.Model):
    patrocinador = models.ForeignKey(Patrocinador, on_delete=models.CASCADE)
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE)


class PatrocinioJogador(models.Model):
    patrocinador = models.ForeignKey(Patrocinador, on_delete=models.CASCADE)
    jogador = models.ForeignKey(Jogador, on_delete=models.CASCADE)
