from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from posts.models import Post, Group
import uuid

User = get_user_model()

class PostViewsTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаём уникального пользователя
        cls.user = User.objects.create_user(username=f'user_{uuid.uuid4()}', password='password')
        # Создаём группу
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Описание группы'
        )
        # Создаём пост
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=cls.group
        )
        # Создаём клиента, авторизированного
        cls.authorized_client = cls.client
        cls.authorized_client.force_login(cls.user)

    def test_post_detail_url_exists(self):
        url = reverse('posts:post_detail', args=[self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_edit_url_exists_for_author(self):
        url = reverse('posts:post_edit', args=[self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_edit_url_redirect_for_anonymous(self):
        url = reverse('posts:post_edit', args=[self.post.id])
        response = self.client.get(url)
        self.assertIn(response.status_code, (301, 302))
        # Можно проверить редирект на авторизацию

    # Можно добавить тесты на правильность шаблонов и контекстов

