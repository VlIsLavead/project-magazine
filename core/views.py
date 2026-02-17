from django.shortcuts import render


def home(request):
    """Главная страница — простой вывод каталога или приветствия."""
    return render(request, 'core/home.html')

