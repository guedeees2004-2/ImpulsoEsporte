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
    list_display = ('username', 'email', 'tipo_conta', 'is_staff', 'is_superuser', 'is_active')
    list_filter = ('tipo_conta', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'tipo_conta')}),
        ('Permissões', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'tipo_conta', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)
    
    def get_queryset(self, request):
        """Personaliza o queryset para filtrar superusers se necessário"""
        qs = super().get_queryset(request)
        return qs
    
    def formfield_for_choice_field(self, db_field, request, **kwargs):
        """Personaliza as opções do campo tipo_conta baseado no usuário"""
        if db_field.name == "tipo_conta":
            # Se está editando um usuário existente
            if hasattr(request, '_editing_user_obj') and request._editing_user_obj and request._editing_user_obj.is_superuser:
                # Para superusers, não mostrar opção de atleta
                kwargs["choices"] = [
                    ('', 'Selecione o tipo de conta'),
                    ('patrocinador', 'Patrocinador'),
                    ('equipe', 'Equipe'),
                    ('outro', 'Outro'),
                ]
        return super().formfield_for_choice_field(db_field, request, **kwargs)
    
    def get_fieldsets(self, request, obj=None):
        """Personaliza fieldsets baseado no tipo de usuário"""
        fieldsets = super().get_fieldsets(request, obj)
        
        # Se é um superuser, adicionar uma nota explicativa
        if obj and obj.is_superuser:
            fieldsets = list(fieldsets)
            # Modificar o fieldset de permissões para incluir uma nota
            for i, (name, options) in enumerate(fieldsets):
                if name == 'Permissões':
                    fieldsets[i] = (name, {
                        **options,
                        'description': '⚠️ Este é um superuser. O tipo de conta é limitado por segurança (não pode ser "atleta").'
                    })
                    break
        
        return fieldsets

    def get_readonly_fields(self, request, obj=None):
        """Define campos somente leitura baseado no tipo de usuário"""
        readonly_fields = list(super().get_readonly_fields(request, obj))
        
        # Se é um superuser sendo editado, tornar tipo_conta somente leitura
        # para evitar mudanças acidentais
        if obj and obj.is_superuser:
            if 'tipo_conta' not in readonly_fields:
                readonly_fields.append('tipo_conta')
        
        return readonly_fields

    def get_form(self, request, obj=None, **kwargs):
        """Passa o objeto para o request para uso no formfield_for_choice_field"""
        request._editing_user_obj = obj
        return super().get_form(request, obj, **kwargs)


@admin.register(Esporte)
class EsporteAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Equipe)
class EquipeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'esporte', 'localizacao', 'get_jogadores_count')
    search_fields = ('nome', 'esporte', 'localizacao')
    list_filter = ('esporte',)
    
    def get_jogadores_count(self, obj):
        return obj.jogador_set.count()
    get_jogadores_count.short_description = 'Nº de Atletas'

@admin.register(Jogador)
class JogadorAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'idade', 'esporte', 'equipe')
    search_fields = ('usuario__username',)
    list_filter = ('esporte', 'equipe')
    autocomplete_fields = ['usuario', 'esporte', 'equipe']
    fieldsets = (
        ('Informações do Atleta', {
            'fields': ('usuario', 'idade', 'esporte')
        }),
        ('Vinculação de Equipe', {
            'fields': ('equipe',),
            'description': 'Selecione a equipe a qual este atleta pertence'
        }),
    )

@admin.register(Patrocinador)
class PatrocinadorAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'empresa', 'cnpj', 'site')
    search_fields = ('empresa', 'cnpj')
    fieldsets = (
        ('Informações Básicas', {'fields': ('usuario', 'empresa', 'cnpj')}),
        ('Contato', {'fields': ('site', 'logo')}),
        ('Informações Adicionais', {'fields': ('descricao',)}),
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
    list_display = ('nome', 'modalidade', 'cidade', 'numero_atletas', 'data_atualizacao')
    list_filter = ('modalidade', 'cidade', 'ano_fundacao')
    search_fields = ('nome', 'modalidade', 'cidade', 'descricao')
    ordering = ('-data_atualizacao',)
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'modalidade', 'cidade', 'ano_fundacao')
        }),
        ('Descrição e Detalhes', {
            'fields': ('descricao', 'numero_atletas')
        }),
        ('Contato', {
            'fields': ('contato_responsavel', 'email_contato'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('data_criacao', 'data_atualizacao')
