from django.shortcuts import render


def index(request):
    context = {
        "title": "Impulso Esporte",
    }
    return render(request, "paginaPrincipal.html", context)


def contato(request):
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
