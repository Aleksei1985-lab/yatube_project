from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.urls import reverse

from posts.models import Post, Group, Comment

User = get_user_model()

class PostImageTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост с картинкой',
            group=cls.group,
            image=cls.uploaded
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_image_in_context(self):
        """Изображение передается в контексте страниц"""
        urls = [
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': self.group.slug}),
            reverse('posts:profile', kwargs={'username': self.user.username}),
            reverse('posts:post_detail', kwargs={'post_id': self.post.id}),
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                if url == reverse('posts:post_detail', kwargs={'post_id': self.post.id}):
                    post = response.context['post']
                else:
                    self.assertEqual(len(response.context['page_obj']), 1)
                    post = response.context['page_obj'][0]
                self.assertEqual(post.image, self.post.image)

    def test_image_in_database(self):
        """При отправке поста с картинкой создается запись в БД"""
        posts_count = Post.objects.count()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small_new.gif',
            content=small_gif,
            content_type='image/gif'
        )
        form_data = {
            'text': 'Новый пост с картинкой',
            'group': self.group.id,
            'image': uploaded,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': self.user.username}))
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text='Новый пост с картинкой',
                group=self.group,
                image__isnull=False
            ).exists()
        )

class CommentTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост'
        )

    def setUp(self):
        self.client = Client()
        self.auth_client = Client()
        self.auth_client.force_login(self.user)

    def test_comment_display(self):
        """Комментарии отображаются на странице поста"""
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            text='Тестовый комментарий'
        )
        response = self.client.get(reverse('posts:post_detail', args=[self.post.id]))
        self.assertContains(response, comment.text)
        self.assertContains(response, comment.author.username)

    def test_comment_auth_required(self):
        """Только авторизованные пользователи могут комментировать"""
        response = self.client.post(
            reverse('posts:add_comment', args=[self.post.id]),
            {'text': 'Новый комментарий'},
            follow=True
        )
        self.assertRedirects(
            response,
            f'/auth/login/?next=/posts/{self.post.id}/comment/'
        )
        self.assertEqual(Comment.objects.count(), 0)

    def test_add_comment(self):
        """Авторизованный пользователь может добавить комментарий"""
        comments_count = Comment.objects.count()
        response = self.auth_client.post(
            reverse('posts:add_comment', args=[self.post.id]),
            {'text': 'Новый комментарий'},
            follow=True
        )
        self.assertEqual(Comment.objects.count(), comments_count + 1)
        self.assertRedirects(response, reverse('posts:post_detail', args=[self.post.id]))
        self.assertContains(response, 'Новый комментарий')