from django.http import HttpResponse
from django.shortcuts import render, reverse
from datetime import datetime
from os import listdir

def home_view(request):
    template_name = 'app/home.html'
    # впишите правильные адреса страниц, используя
    # функцию `reverse`
    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время': reverse('time'),
        'Показать содержимое рабочей директории': reverse('workdir')
    }
    
    # context и параметры render менять не нужно
    # подбробнее о них мы поговорим на следующих лекциях
    context = {
        'pages': pages
    }
    return render(request, template_name, context)


def time_view(request):
    # обратите внимание – здесь HTML шаблона нет, 
    # возвращается просто текст
    current_time = datetime.now().strftime('%H:%M:%S')
    msg = f'Текущее время: {current_time}'
    return HttpResponse(msg)


def workdir_view(request):
    # по аналогии с `time_view`, напишите код,
    # который возвращает список файлов в рабочей 
    # директории
    current_dir = listdir('.')
    header = '''<head><meta charset="UTF-8" name="viewport" content="width=device-width, initial-scale=1"></head>
                <link rel="stylesheet" href="https://stackedit.io/style.css" />
                <body class="stackedit"><div class="stackedit__html">
                <div class="stackedit__html">
                '''
    msg = '<h2>Содержимое рабочей директории:</h2>'
    for dir in current_dir:
        msg += f'<li>{dir}</li>\n'
    msg = header + msg + '</div></body>'
    return HttpResponse(msg)
    
