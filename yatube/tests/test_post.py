import pytest
from django import forms
from posts.forms import PostForm
from posts.models import Post
from django.urls import reverse
from tests.utils import get_field_from_context
import uuid

class TestPostView:

    @pytest.mark.django_db(transaction=True)
    def test_post_view_get(self, client, post_with_group):
        try:
            response = client.get(f'/posts/{post_with_group.id}')
        except Exception as e:
            assert False, f'''Страница `/posts/<post_id>/` работает неправильно. Ошибка: `{e}`'''
        if response.status_code in (301, 302):
            response = client.get(f'/posts/{post_with_group.id}/')
        assert response.status_code != 404, (
            'Страница `/posts/<post_id>/` не найдена, проверьте этот адрес в *urls.py*'
        )

        post_context = get_field_from_context(response.context, Post)
        assert post_context is not None, (
            'Проверьте, что передали статью в контекст страницы `/posts/<post_id>/` типа `Post`'
        )


class TestPostEditView:

    @pytest.mark.django_db(transaction=True)
    def test_post_edit_view_get(self, client, post_with_group):
        try:
            response = client.get(f'/posts/{post_with_group.id}/edit')
        except Exception as e:
            assert False, f'''Страница `/posts/<post_id>/edit/` работает неправильно. Ошибка: `{e}`'''
        if (
                response.status_code in (301, 302)
                and not response.url.startswith(f'/posts/{post_with_group.id}')
        ):
            response = client.get(f'/posts/{post_with_group.id}/edit/')
        assert response.status_code != 404, (
            'Страница `/posts/<post_id>/edit/` не найдена, проверьте этот адрес в *urls.py*'
        )

        assert response.status_code in (301, 302), (
            'Проверьте, что вы переадресуете пользователя со страницы '
            '`/<username>/<post_id>/edit/` на страницу поста, если он не автор'
        )

    @pytest.mark.django_db(transaction=True)
    def test_post_edit_view_author_get(self, user_client, post_with_group):
        print(f"Post author: {post_with_group.author.username}")  # автор поста
        print(f"User: {user_client.session['_auth_user_id']}")  # ID авторизованного пользователя
        
        response = user_client.get(f'/posts/{post_with_group.id}/edit/')
        print(f"Status code: {response.status_code}")
        
        if response.context:
            print(f"Context keys: {response.context.keys()}")
        else:
            print("Context is None")
        
        assert response.status_code == 200, "Страница должна возвращать код 200"
        assert response.context is not None, "Контекст не передан в шаблон"
        assert 'form' in response.context, "Форма не передана в контекст"
        try:
            response = user_client.get(f'/posts/{post_with_group.id}/edit')
        except Exception as e:
            assert False, f'''Страница `/posts/<post_id>/edit/` работает неправильно. Ошибка: `{e}`'''
        if response.status_code in (301, 302):
            response = user_client.get(f'/posts/{post_with_group.id}/edit/')
        assert response.status_code != 404, (
            'Страница `/posts/<post_id>/edit/` не найдена, проверьте этот адрес в *urls.py*'
        )

        post_context = get_field_from_context(response.context, Post)
        postform_context = get_field_from_context(response.context, PostForm)
        assert any([post_context, postform_context]) is not None, (
            'Проверьте, что передали статью в контекст страницы `/posts/<post_id>/edit/` типа `Post` или `PostForm`'
        )

        assert 'form' in response.context, (
            'Проверьте, что передали форму `form` в контекст страницы `/posts/<post_id>/edit/`'
        )
        assert len(response.context['form'].fields) == 3, (
            'Проверьте, что в форме `form` на страницу `/posts/<post_id>/edit/` 3 поля'
        )
        assert 'group' in response.context['form'].fields, (
            'Проверьте, что в форме `form` на странице `/posts/<post_id>/edit/` есть поле `group`'
        )
        assert type(response.context['form'].fields['group']) == forms.models.ModelChoiceField, (
            'Проверьте, что в форме `form` на странице `/posts/<post_id>/edit/` поле `group` типа `ModelChoiceField`'
        )
        assert not response.context['form'].fields['group'].required, (
            'Проверьте, что в форме `form` на странице `/posts/<post_id>/edit/` поле `group` не обязательно'
        )

        assert 'text' in response.context['form'].fields, (
            'Проверьте, что в форме `form` на странице `/posts/<post_id>/edit/` есть поле `text`'
        )
        assert type(response.context['form'].fields['text']) == forms.fields.CharField, (
            'Проверьте, что в форме `form` на странице `/posts/<post_id>/edit/` поле `text` типа `CharField`'
        )
        assert response.context['form'].fields['text'].required, (
            'Проверьте, что в форме `form` на странице `/posts/<post_id>/edit/` поле `group` обязательно'
        )

    @pytest.mark.django_db(transaction=True)
    def test_post_edit_view_author_post(self, user_client, post_with_group):
        response = user_client.get(reverse('posts:post_edit', args=[post_with_group.id]))
        assert response.status_code == 200
        new_text = 'Новый текст поста'
        url = f'/posts/{post_with_group.id}/edit/'
        
        # Проверяем исходное состояние
        print(f"Original text: {post_with_group.text}")
        
        response = user_client.post(url, {
            'text': new_text,
            'group': post_with_group.group_id
        }, follow=True)  # follow=True для следования за редиректом
        
        print(f"Status code: {response.status_code}")
        print(f"Redirect chain: {response.redirect_chain}")
        
        # Проверяем обновление в БД
        updated_post = Post.objects.get(id=post_with_group.id)
        print(f"Updated text: {updated_post.text}")
        
        assert updated_post.text == new_text, "Текст поста не обновился"
        text = 'Проверка изменения поста!'
        try:
            response = user_client.get(f'/posts/{post_with_group.id}/edit')
        except Exception as e:
            assert False, f'''Страница `/posts/<post_id>/edit/` работает неправильно. Ошибка: `{e}`'''
        url = (
            f'/posts/{post_with_group.id}/edit/'
            if response.status_code in (301, 302)
            else f'/posts/{post_with_group.id}/edit'
        )

        response = user_client.post(url, data={'text': text, 'group': post_with_group.group_id})

        assert response.status_code in (301, 302), (
            'Проверьте, что со страницы `/posts/<post_id>/edit/` '
            'после создания поста перенаправляете на страницу поста'
        )
        post = Post.objects.filter(author=post_with_group.author, text=text, group=post_with_group.group).first()
        assert post is not None, (
            'Проверьте, что вы изменили пост при отправки формы на странице `/posts/<post_id>/edit/`'
        )
        assert response.url.startswith(f'/posts/{post_with_group.id}'), (
            'Проверьте, что перенаправляете на страницу поста `/posts/<post_id>/`'
        )
