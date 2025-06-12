from django.shortcuts import render

def index(request):
    context = {
        "title": "Impulse Esporte",
    }
    return render(request, "index.html", context)
