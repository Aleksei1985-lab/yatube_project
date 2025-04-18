from django.test import TestCase
from posts.models import Post, Group
from django.contrib.auth import get_user_model

User = get_user_model()

class PostModelTest(TestCase):
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

    def test_help_text(self):
        """Проверяем help_text в полях."""
        field_help_texts = {
            'text': 'Текст нового поста',
            'group': 'Группа, к которой будет относиться пост',
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    Post._meta.get_field(field).help_text,
                    expected_value
                )

    def test_str_method(self):
        """Проверяем __str__ моделей."""
        self.assertEqual(str(self.post), self.post.text[:15])
        self.assertEqual(str(self.group), self.group.title)