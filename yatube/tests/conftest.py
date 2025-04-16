import pytest
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yatube.settings')
django.setup()
from django.contrib.auth import get_user_model
from posts.models import Post, Group

User = get_user_model()

@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='12345')

@pytest.fixture
def user_client(user, client):
    client.force_login(user)
    return client

@pytest.fixture
def group():
    return Group.objects.create(
        title='Test group',
        slug='test-slug',
        description='Test description'
    )

@pytest.fixture
def post_with_group(user, group):
    return Post.objects.create(
        text='Test post',
        author=user,
        group=group
    )

@pytest.fixture
def few_posts_with_group(user, group):
    posts = []
    for i in range(15):
        posts.append(Post(
            text=f'Test post {i}',
            author=user,
            group=group
        ))
    return Post.objects.bulk_create(posts)