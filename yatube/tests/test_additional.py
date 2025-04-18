from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from posts.models import Post, Group
import time

User = get_user_model()

class AdditionalTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        # Создаем 13 тестовых постов
        for i in range(13):
            Post.objects.create(
                author=cls.user,
                text=f'Тестовый пост {i}',
                group=cls.group
            )
        cls.client = Client()

    def test_index_cache(self):
        """Проверка кеширования главной страницы."""
        from django.core.cache import cache
        cache.clear()  # Очищаем кэш перед тестом
        
        # Создаем уникальный текст
        unique_text = f"Тест кэширования {time.time()}"
        post = Post.objects.create(
            author=self.user,
            text=unique_text,
            group=self.group,
            image=None  # Явно указываем отсутствие изображения
        )
        
        # Первый запрос - должен закешироваться
        response1 = self.client.get(reverse('posts:index'))
        self.assertEqual(response1.status_code, 200)
        self.assertContains(response1, unique_text)
        
        # Удаляем пост из БД
        post.delete()
        
        # Второй запрос - должен быть из кэша
        response2 = self.client.get(reverse('posts:index'))
        self.assertContains(response2, unique_text)
        
        # Очищаем кэш
        cache.clear()
        
        # Третий запрос - поста не должно быть
        response3 = self.client.get(reverse('posts:index'))
        self.assertNotContains(response3, unique_text)

    def test_paginator(self):
        """Проверка пагинации."""
        urls = [
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': 'test-slug'}),
            reverse('posts:profile', kwargs={'username': 'auth'}),
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(len(response.context['page_obj']), 10)
                response = self.client.get(url + '?page=2')
                self.assertEqual(len(response.context['page_obj']), 3)