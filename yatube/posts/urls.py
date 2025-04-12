from django.urls import path

from . import views

app_name = 'posts'  # Пространство имен приложения

urlpatterns = [
    path('', views.index, name='index'),  # Главная страница
    path('group/<slug:slug>/', views.group_posts, name='group_list'),  # Страница группы
]