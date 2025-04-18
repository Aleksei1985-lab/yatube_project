from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from posts.models import Post, Group

User = get_user_model()

class PostViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=cls.group
        )
        cls.client = Client()
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list', kwargs={'slug': 'test-slug'}): 'posts/group_list.html',
            reverse('posts:profile', kwargs={'username': 'auth'}): 'posts/profile.html',
            reverse('posts:post_detail', kwargs={'post_id': 1}): 'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse('posts:post_edit', kwargs={'post_id': 1}): 'posts/create_post.html',
        }
        
        for reverse_name, template in templates.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertEqual(response.status_code, 200)  # Сначала проверяем успешность запроса
                self.assertTemplateUsed(response, template)