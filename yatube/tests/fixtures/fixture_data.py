import pytest
from mixer.backend.django import mixer
from yatube.models import Post, Group

@pytest.fixture
def user_client(client, user):
    client.force_login(user)
    return client

@pytest.fixture
def group(db):
    return Group.objects.create(
        title='Test Group',
        slug='test-group',
        description='Test description'
    )

@pytest.fixture
def post_with_group(db, user, group):
    return Post.objects.create(
        text='Test post',
        author=user,
        group=group
    )