from django.shortcuts import render, redirect
from django.contrib import messages


def index(request):
    context = {
        "title": "Impulso Esporte",
    }
    return render(request, "paginaPrincipal.html", context)


def contato(request):
    if request.method == 'POST':
        # Processar os dados do formulário
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        mensagem = request.POST.get('mensagem')
        
        # Aqui você pode adicionar lógica para salvar no banco ou enviar por email
        # Por enquanto, vamos apenas mostrar uma mensagem de sucesso
        
        if nome and email and mensagem:
            messages.success(request, 'Sua mensagem foi enviada com sucesso! Entraremos em contato em breve.')
            return redirect('contato')  # Redireciona para evitar reenvio do formulário
        else:
            messages.error(request, 'Por favor, preencha todos os campos obrigatórios.')
    
    context = {
        "title": "Impulso Esporte - Contato",
    }
    return render(request, "contato.html", context)


def pagina_sobre_nos(request):
    context = {
        "title": "Sobre Nós - Impulso Esporte",
    }
    return render(request, "paginaSobreNos.html", context)


def servicos(request):
    context = {
        "title": "Serviços - Impulso Esporte",
    }
    return render(request, "servicos.html", context)
