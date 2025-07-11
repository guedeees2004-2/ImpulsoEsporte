# Vinculação entre Atletas e Equipes

## Como Vincular Atletas a Equipes

A vinculação entre atletas e equipes é feita através do painel administrativo do Django.

### Passo a Passo:

1. **Acesse o Painel Admin**
   - Vá para: `http://localhost:8000/admin/`
   - Faça login com uma conta de administrador

2. **Criar/Editar um Jogador**
   - Clique em "Jogadors" na seção "APPIMPULSOESPORTE"
   - Para criar novo: clique em "Adicionar Jogador"
   - Para editar existente: clique no jogador desejado

3. **Configurar a Vinculação**
   - **Usuário**: Selecione o usuário que é atleta
   - **Posição**: Defina a posição do atleta
   - **Idade**: Informe a idade
   - **Esporte**: Selecione o esporte
   - **Equipe**: **AQUI é onde você vincula** - selecione a equipe

4. **Salvar**
   - Clique em "Salvar" para confirmar a vinculação

### Resultado da Vinculação:

**Na Página do Atleta:**
- Aparecerá a seção "Minha Equipe"
- Mostrará nome, modalidade e localização da equipe
- Terá botão para acessar a página da equipe

**Na Página da Equipe:**
- Os atletas vinculados aparecerão na seção "Nossos Atletas"
- Mostrará nome, posição, idade
- Terá botão para ver o perfil do atleta

### Observações:

- Um atleta pode estar vinculado a apenas uma equipe por vez
- Para desvincular, edite o jogador e deixe o campo "Equipe" em branco
- A vinculação é bidirecional: aparece tanto na página do atleta quanto da equipe

### Estrutura dos Modelos:

```python
# Jogador (representa os atletas)
- usuario: link para o Usuario
- equipe: link para a Equipe (ESTE é o campo de vinculação)
- posicao: texto da posição
- idade: número
- esporte: link para Esporte

# Equipe
- nome: nome da equipe
- esporte: modalidade esportiva
- localizacao: onde fica a equipe
```
