from json import loads
from datetime import datetime
from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi
from restclient.configuration import Configuration as MailhogConfiguration, Configuration as DmApiConfiguration
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True)
    ]
)

def test_post_v1_account():
    # Регистрация пользователя
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025', disable_log=True)
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)

    account_api = AccountApi(configuration=dm_api_configuration)
    login_api = LoginApi(configuration=dm_api_configuration)
    mailhog_api = MailhogApi(configuration=mailhog_configuration)

    now_date = datetime.now()
    login = f"s-test-{now_date.strftime('%Y%m%d%H%M%S')}"
    password = '12345678'
    email = f'{login}@m.ru'
    json_data = {
        'login': login,
        'email': email,
        'password': password
    }

    response = account_api.post_v1_account(json_data=json_data)

    assert response.status_code == 201, f"Пользователь не создан {response.json()}"
    # Получить письма из почтового сервера

    response = mailhog_api.get_api_v2_messages()

    assert response.status_code == 200, "Письма не получены"

    # Получить активационный токен
    token = get_activation_token_by_login(login, email, response)

    assert token is not None, f"Токен для пользователя {login}, не был получен"

    # Активация пользователя
    response = account_api.put_v1_account_token(token=token)

    assert response.status_code == 200, "Пользователь не был активирован"

    # Авторизация
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)

    assert response.status_code == 200, "Пользователь не был авторизован"


def get_activation_token_by_login(
        login,
        email,
        response
        ):
    token = None
    # pprint.pprint(response.json())
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data.get('Login')
        user_email = item['Content']['Headers']['To'][0]
        print(f"Проверка письма: login={user_login}, email={user_email}")
        if user_login == login and user_email == email:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
            print(f"Найден токен: {token}")
            break
    return token






