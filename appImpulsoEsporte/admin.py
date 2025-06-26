from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Usuario,
    Esporte,
    Equipe,
    Jogador,
    Patrocinador,
    PatrocinioEquipe,
    PatrocinioJogador
)

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('username', 'email', 'tipo_conta', 'is_staff', 'is_active')
    list_filter = ('tipo_conta', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'tipo_conta')}),
        ('Permissões', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'tipo_conta', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)


@admin.register(Esporte)
class EsporteAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Equipe)
class EquipeAdmin(admin.ModelAdmin):
    list_display = ('nome_da_equipe', 'esporte')
    search_fields = ('nome_da_equipe',)
    list_filter = ('esporte',)

@admin.register(Jogador)
class JogadorAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'posicao', 'idade', 'esporte', 'equipe')
    search_fields = ('usuario__username', 'posicao')
    list_filter = ('esporte', 'equipe')

@admin.register(Patrocinador)
class PatrocinadorAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'empresa', 'cnpj', 'aberto_para_oportunidades')
    search_fields = ('empresa', 'cnpj')
    list_filter = ('aberto_para_oportunidades',)
    fieldsets = (
        (None, {'fields': ('usuario', 'empresa', 'cnpj')}),
        ('Disponibilidade', {'fields': ('aberto_para_oportunidades', 'descricao')}),
    )

@admin.register(PatrocinioEquipe)
class PatrocinioEquipeAdmin(admin.ModelAdmin):
    list_display = ('patrocinador', 'equipe')
    search_fields = ('patrocinador__empresa', 'equipe__nome_da_equipe')

@admin.register(PatrocinioJogador)
class PatrocinioJogadorAdmin(admin.ModelAdmin):
    list_display = ('patrocinador', 'jogador')
    search_fields = ('patrocinador__empresa', 'jogador__usuario__username')


# Register Usuario with custom admin class
# Note: We don't need to call admin.site.register again since we use @admin.register decorator above
