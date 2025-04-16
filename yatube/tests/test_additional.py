# posts/tests/test_additional.py
from django.test import TestCase, Client
from django.urls import reverse
from django.core.cache import cache
from django.contrib.auth import get_user_model
from posts.models import Post, Group

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
        for i in range(13):
            Post.objects.create(
                author=cls.user,
                text=f'Тестовый пост {i}',
                group=cls.group
            )

    def setUp(self):
        self.guest_client = Client()
        cache.clear()

    def test_index_cache(self):
        cache.clear()  # Очистка кэша перед тестом
        response_before = self.guest_client.get(reverse('posts:index'))
        Post.objects.create(
            author=self.user,
            text='Новый пост для проверки кэша',
        )
        response_after = self.guest_client.get(reverse('posts:index'))
        self.assertEqual(response_before.content, response_after.content)

    def test_paginator(self):
        """Проверка пагинации."""
        urls = [
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': 'test-slug'}),
            reverse('posts:profile', kwargs={'username': 'auth'}),
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(len(response.context['page_obj']), 10)
                response = self.guest_client.get(url + '?page=2')
                self.assertEqual(len(response.context['page_obj']), 3)