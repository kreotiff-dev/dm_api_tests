import pprint

import requests
from json import loads


def test_post_v1_account():
    # Регистрация пользователя
    account_api = AccountApi
    login = 's-test2'
    password = '12345678'
    email = f'{login}@m.ru'
    json_data = {
        'login': login,
        'email': email,
        'password': password
    }

    response = post_v1_account(json_data)
    print(response.status_code)
    print(response.text)

    assert response.status_code == 201, f"Пользователь не создан {response.json()}"
    # Получить письма из почтового сервера

    response = get_api_v2_messages(response)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Письма не получены"

    # Получить активационный токен
    token = get_activation_token_by_login(login, response)

    assert token is not None, f"Токен для пользователя {login}, не был получен"

    # Активация пользователя
    response = put_v1_account_token(token)
    print(response.status_code)
    print(response.text)

    assert response.status_code == 200, "Пользователь не был активирован"

    # Авторизация
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = post_v1_account_login(json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Пользователь не был авторизован"








def get_activation_token_by_login(login, response):
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
    return token






