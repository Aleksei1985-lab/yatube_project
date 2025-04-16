import pytest




def test_auth_urls(client):
    urls = [
        ('/auth/login/', 200),
        ('/auth/signup/', 200),
        ('/auth/logout/', 405)  # Ожидаем 405 для GET-запроса
    ]
    for url, expected_code in urls:
        try:
            response = client.get(url)
        except Exception as e:
            assert False, f'''Страница `{url}` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code != 404, f'Страница `{url}` не найдена, проверьте этот адрес в *urls.py*'
        assert response.status_code == expected_code, (
            f'Ошибка {response.status_code} при открытиии `{url}`. Ожидался {expected_code}'
        )