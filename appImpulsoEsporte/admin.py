from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Usuario,
    Esporte,
    Equipe,
    Jogador,
    Patrocinador,
    PatrocinioEquipe,
    PatrocinioJogador,
    EquipeDisponivel
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
    list_display = ('nome', 'esporte', 'localizacao')
    search_fields = ('nome',)
    list_filter = ('esporte',)

@admin.register(Jogador)
class JogadorAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'posicao', 'idade', 'esporte', 'equipe')
    search_fields = ('usuario__username', 'posicao')
    list_filter = ('esporte', 'equipe')

@admin.register(Patrocinador)
class PatrocinadorAdmin(admin.ModelAdmin):
<<<<<<< HEAD
    list_display = ('usuario', 'empresa', 'cnpj', 'aberto_para_oportunidades','site')
=======
    list_display = ('usuario', 'empresa', 'cnpj', 'site_empresa')
>>>>>>> cfa3559e18942aaf24e8e64ad8730dfd37312b12
    search_fields = ('empresa', 'cnpj')
    fieldsets = (
<<<<<<< HEAD
        (None, {'fields': ('usuario', 'empresa', 'cnpj', 'site', 'logo')}),
        ('Disponibilidade', {'fields': ('aberto_para_oportunidades', 'descricao')}),
=======
        ('Informações Básicas', {'fields': ('usuario', 'empresa', 'cnpj')}),
        ('Contato', {'fields': ('site_empresa',)}),
        ('Informações Adicionais', {'fields': ('descricao',)}),
>>>>>>> cfa3559e18942aaf24e8e64ad8730dfd37312b12
    )

@admin.register(PatrocinioEquipe)
class PatrocinioEquipeAdmin(admin.ModelAdmin):
    list_display = ('patrocinador', 'equipe')
    search_fields = ('patrocinador__empresa', 'equipe__nome')

@admin.register(PatrocinioJogador)
class PatrocinioJogadorAdmin(admin.ModelAdmin):
    list_display = ('patrocinador', 'jogador')
    search_fields = ('patrocinador__empresa', 'jogador__usuario__username')

@admin.register(EquipeDisponivel)
class EquipeDisponivelAdmin(admin.ModelAdmin):
    model = EquipeDisponivel
    list_display = ('nome', 'modalidade', 'cidade', 'aberta_para_atletas', 'numero_atletas', 'data_atualizacao')
    list_filter = ('modalidade', 'cidade', 'aberta_para_atletas', 'ano_fundacao')
    search_fields = ('nome', 'modalidade', 'cidade', 'descricao')
    ordering = ('-data_atualizacao',)
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'modalidade', 'cidade', 'ano_fundacao')
        }),
        ('Descrição e Detalhes', {
            'fields': ('descricao', 'numero_atletas', 'aberta_para_atletas')
        }),
        ('Contato', {
            'fields': ('contato_responsavel', 'email_contato'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('data_criacao', 'data_atualizacao')

# Register Usuario with custom admin class
# Note: We don't need to call admin.site.register again since we use @admin.register decorator above
