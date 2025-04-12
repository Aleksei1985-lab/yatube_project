from django.shortcuts import render

def index(request):
    context = {
        'title': 'Это главная страница проекта Yatube'
    }
    return render(request, 'posts/index.html', context)

def group_posts(request, slug):
    context = {
        'title': f'Здесь будет информация о группах проекта Yatube {slug}'
    }
    return render(request, 'posts/group_list.html', context)
